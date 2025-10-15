import random

# --- CONFIGURATION & INPUT DATA (This would come from the web form) ---
# For simplicity, we define it here. In the real app, this data is passed to run_scheduler().
ROOMS = ["R1", "R2", "R3"]
TIMESLOTS = ["9-10", "10-11", "11-12", "1-2", "2-3"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
FACULTY = {
    "F1": {"name": "Dr. Smith", "subjects": ["CS101", "AI201"]},
    "F2": {"name": "Dr. Jones", "subjects": ["MA101", "CS101"]},
    "F3": {"name": "Dr. Williams", "subjects": ["EE201"]},
}
SUBJECTS = {
    "CS101": {"name": "Intro to CS", "hours_per_week": 3, "batches": ["B1", "B2"]},
    "MA101": {"name": "Maths I", "hours_per_week": 4, "batches": ["B1", "B2"]},
    "AI201": {"name": "Intro to AI", "hours_per_week": 2, "batches": ["B1"]},
    "EE201": {"name": "Basic Electronics", "hours_per_week": 3, "batches": ["B2"]},
}
BATCHES = ["B1", "B2"]

POPULATION_SIZE = 100
MAX_GENERATIONS = 500
MUTATION_RATE = 0.1

# A "gene" represents one class session: (Day, Timeslot, Room, Batch, Subject, Faculty)
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

# A "chromosome" is a full timetable (a list of genes)
class Timetable:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        conflicts = 0
        # Hard Constraint 1: A teacher cannot be in two places at once.
        teacher_slots = {}
        for gene in self.genes:
            key = (gene.day, gene.timeslot, gene.faculty)
            if key in teacher_slots:
                conflicts += 1
            else:
                teacher_slots[key] = True

        # Hard Constraint 2: A room cannot be occupied by two classes at once.
        room_slots = {}
        for gene in self.genes:
            key = (gene.day, gene.timeslot, gene.room)
            if key in room_slots:
                conflicts += 1
            else:
                room_slots[key] = True

        # Hard Constraint 3: A batch cannot attend two classes at once.
        batch_slots = {}
        for gene in self.genes:
            key = (gene.day, gene.timeslot, gene.batch)
            if key in batch_slots:
                conflicts += 1
            else:
                batch_slots[key] = True

        # Soft Constraint 1: Check if subjects get their required hours per week
        subject_hours = {batch: {sub: 0 for sub in SUBJECTS} for batch in BATCHES}
        for gene in self.genes:
            if gene.subject in subject_hours.get(gene.batch, {}):
                 subject_hours[gene.batch][gene.subject] += 1
        
        for batch, subs in subject_hours.items():
            for sub_code, required_hours in SUBJECTS.items():
                if sub_code in subs:
                    # Penalize for not meeting the required hours
                    conflicts += abs(subs[sub_code] - required_hours['hours_per_week'])

        return conflicts

# --- GENETIC ALGORITHM FUNCTIONS ---

def create_individual(all_possible_genes):
    """Creates a single random timetable."""
    # This should create a timetable with the correct number of classes per subject
    genes = []
    for subject_code, details in SUBJECTS.items():
        for batch in details['batches']:
            for _ in range(details['hours_per_week']):
                # Find a faculty who can teach this subject
                possible_faculty = [f_id for f_id, f_details in FACULTY.items() if subject_code in f_details['subjects']]
                if not possible_faculty: continue # Skip if no teacher available
                
                gene = Gene(
                    day=random.choice(DAYS),
                    timeslot=random.choice(TIMESLOTS),
                    room=random.choice(ROOMS),
                    batch=batch,
                    subject=subject_code,
                    faculty=random.choice(possible_faculty)
                )
                genes.append(gene)
    return Timetable(genes)


def create_population(size):
    """Creates an initial population of random timetables."""
    return [create_individual(None) for _ in range(size)]

def selection(population):
    """Selects two 'parent' timetables based on fitness."""
    # Tournament selection
    tournament = random.sample(population, 5)
    fittest = sorted(tournament, key=lambda x: x.fitness)[0]
    return fittest

def crossover(parent1, parent2):
    """Creates a 'child' timetable by combining two parents."""
    crossover_point = random.randint(1, len(parent1.genes) - 1)
    child1_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
    child2_genes = parent2.genes[:crossover_point] + parent1.genes[crossover_point:]
    return Timetable(child1_genes), Timetable(child2_genes)

def mutate(timetable):
    """Applies random changes to a timetable."""
    if random.random() < MUTATION_RATE:
        gene_to_mutate = random.choice(timetable.genes)
        gene_to_mutate.day = random.choice(DAYS)
        gene_to_mutate.timeslot = random.choice(TIMESLOTS)
        gene_to_mutate.room = random.choice(ROOMS)
    return timetable

# --- MAIN SCHEDULER FUNCTION ---

def run_scheduler(input_data):
    # In a real app, you would parse input_data to update the global config variables
    # For now, we use the predefined global variables
    
    population = create_population(POPULATION_SIZE)
    
    for generation in range(MAX_GENERATIONS):
        population = sorted(population, key=lambda x: x.fitness)
        
        # If we found a perfect solution, stop
        if population[0].fitness == 0:
            print(f"Solution found in generation {generation}!")
            return population[0]

        # Create the next generation
        next_generation = []
        # Keep the best 10% (elitism)
        elite_count = POPULATION_SIZE // 10
        next_generation.extend(population[:elite_count])

        # Create the rest of the new generation
        while len(next_generation) < POPULATION_SIZE:
            parent1 = selection(population)
            parent2 = selection(population)
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(mutate(child1))
            if len(next_generation) < POPULATION_SIZE:
                next_generation.append(mutate(child2))
        
        population = next_generation
        
        if generation % 50 == 0:
            print(f"Generation {generation}: Best Fitness = {population[0].fitness}")

    # Return the best timetable found after all generations
    best_timetable = sorted(population, key=lambda x: x.fitness)[0]
    print("Finished. Best timetable found has fitness:", best_timetable.fitness)
    return best_timetable