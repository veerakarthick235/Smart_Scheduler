# scheduler_v2.py
import random
from collections import defaultdict

# --- (The Gene and Timetable classes remain exactly the same as before) ---
class Gene:
    def __init__(self, day, timeslot, room, batch, subject, faculty):
        self.day = day
        self.timeslot = timeslot
        self.room = room
        self.batch = batch
        self.subject = subject
        self.faculty = faculty

    def __repr__(self):
        return f"({self.day}, {self.timeslot}, {self.room}, {self.batch}, {self.subject}, {self.faculty})"

class Timetable:
    def __init__(self, genes, config):
        self.genes = genes
        self.config = config
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        conflicts = 0
        
        # --- HARD CONSTRAINTS (High penalty) ---
        teacher_slots = defaultdict(int)
        room_slots = defaultdict(int)
        batch_slots = defaultdict(int)

        for gene in self.genes:
            teacher_slots[(gene.day, gene.timeslot, gene.faculty)] += 1
            room_slots[(gene.day, gene.timeslot, gene.room)] += 1
            batch_slots[(gene.day, gene.timeslot, gene.batch)] += 1

        conflicts += sum(v - 1 for v in teacher_slots.values() if v > 1) * 10
        conflicts += sum(v - 1 for v in room_slots.values() if v > 1) * 10
        conflicts += sum(v - 1 for v in batch_slots.values() if v > 1) * 10

        # --- SOFT CONSTRAINTS (Lower penalty) ---
        for batch in self.config['batches']:
            for day in self.config['days']:
                day_classes = sorted([g for g in self.genes if g.batch == batch and g.day == day], 
                                     key=lambda g: self.config['timeslots'].index(g.timeslot))
                
                consecutive_count = 1
                for i in range(1, len(day_classes)):
                    current_slot_index = self.config['timeslots'].index(day_classes[i].timeslot)
                    prev_slot_index = self.config['timeslots'].index(day_classes[i-1].timeslot)
                    if current_slot_index == prev_slot_index + 1:
                        consecutive_count += 1
                    else:
                        consecutive_count = 1
                    
                    if consecutive_count > 2:
                        conflicts += 1

        return conflicts

# --- (The helper functions like create_individual, selection, crossover, mutate also remain the same) ---
def create_individual(config):
    genes = []
    if not config.get('subjects') or not config.get('rooms'):
        return Timetable([], config) # Return empty timetable if no subjects/rooms

    for subject_code, details in config['subjects'].items():
        for batch in details.get('batches', []):
            for _ in range(details.get('hours_per_week', 0)):
                possible_faculty = [f_name for f_name, f_details in config['faculty'].items() if subject_code in f_details.get('subjects', [])]
                if not possible_faculty: continue
                
                gene = Gene(
                    day=random.choice(config['days']),
                    timeslot=random.choice(config['timeslots']),
                    room=random.choice(config['rooms']),
                    batch=batch,
                    subject=subject_code,
                    faculty=random.choice(possible_faculty)
                )
                genes.append(gene)
    return Timetable(genes, config)

def run_scheduler(input_data):
    # --- CONFIGURATION ---
    POPULATION_SIZE = 100
    MAX_GENERATIONS = 300
    MUTATION_RATE = 0.1
    # --- NEW: STAGNATION CONFIGURATION ---
    # Stop if the best score doesn't improve for this many generations
    STAGNATION_LIMIT = 50 

    # --- Helper functions ---
    def create_population(size, config):
        return [create_individual(config) for _ in range(size)]

    def selection(population):
        tournament = random.sample(population, 5)
        return sorted(tournament, key=lambda x: x.fitness)[0]

    def crossover(parent1, parent2):
        # Gracefully handle cases with very few classes
        if not parent1.genes or not parent2.genes or len(parent1.genes) <= 1:
            return Timetable(parent1.genes, parent1.config), Timetable(parent2.genes, parent2.config)
        
        crossover_point = random.randint(1, len(parent1.genes) - 1)
        child1_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
        child2_genes = parent2.genes[:crossover_point] + parent1.genes[crossover_point:]
        return Timetable(child1_genes, parent1.config), Timetable(child2_genes, parent2.config)

    def mutate(timetable):
        if random.random() < MUTATION_RATE and timetable.genes:
            gene_to_mutate = random.choice(timetable.genes)
            gene_to_mutate.day = random.choice(timetable.config['days'])
            gene_to_mutate.timeslot = random.choice(timetable.config['timeslots'])
            gene_to_mutate.room = random.choice(timetable.config['rooms'])
        timetable.fitness = timetable.calculate_fitness()
        return timetable

    # --- Main GA loop ---
    population = create_population(POPULATION_SIZE, input_data)
    if not population or not population[0].genes:
        print("Warning: Initial population is empty. Check input data (especially faculty-subject assignments).")
        return Timetable([], input_data) # Return an empty result immediately

    # --- NEW: TRACKING VARIABLES FOR STAGNATION ---
    best_fitness_so_far = float('inf')
    generations_without_improvement = 0

    for generation in range(MAX_GENERATIONS):
        population = sorted(population, key=lambda x: x.fitness)
        
        current_best_fitness = population[0].fitness

        # --- NEW: STAGNATION CHECK LOGIC ---
        if current_best_fitness < best_fitness_so_far:
            best_fitness_so_far = current_best_fitness
            generations_without_improvement = 0
            print(f"Gen {generation}: New Best Fitness = {best_fitness_so_far}")
        else:
            generations_without_improvement += 1
        
        # --- MODIFIED EXIT CONDITIONS ---
        # 1. If we found a perfect solution, stop.
        if current_best_fitness == 0:
            print(f"Perfect solution found in generation {generation}!")
            break
        
        # 2. If the solution hasn't improved in a while, stop.
        if generations_without_improvement >= STAGNATION_LIMIT:
            print(f"Stopping early due to stagnation at generation {generation}.")
            break
        # --- END OF MODIFIED LOGIC ---

        # Create the next generation
        next_generation = population[:POPULATION_SIZE // 10]
        while len(next_generation) < POPULATION_SIZE:
            p1, p2 = selection(population), selection(population)
            c1, c2 = crossover(p1, p2)
            next_generation.append(mutate(c1))
            if len(next_generation) < POPULATION_SIZE:
                next_generation.append(mutate(c2))
        
        population = next_generation
    
    best_timetable = sorted(population, key=lambda x: x.fitness)[0]
    print(f"Finished. Best timetable found has fitness: {best_timetable.fitness}")
    return best_timetable