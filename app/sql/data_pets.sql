INSERT INTO
    public.pet (pet_name,pet_type,description,shelter_id)
VALUES
    ('Kulfon','dog','Owczarek niemiecki, ładny piesek, nie ma pcheł', (SELECT id FROM public.shelter OFFSET 5 LIMIT 1)),
    ('Azor','dog','Miły i przyjazny', (SELECT id FROM public.shelter OFFSET 4 LIMIT 1)),
    ('Burek','dog','Szuka nowego domu', (SELECT id FROM public.shelter OFFSET 1 LIMIT 1)),
    ('Tadeusz','cat','Rudy kocur', (SELECT id FROM public.shelter OFFSET 3 LIMIT 1)),
    ('Max','parrot','Głośna', (SELECT id FROM public.shelter OFFSET 2 LIMIT 1)),
    ('Mateusz','parrot','Naśladuje ludzi', (SELECT id FROM public.shelter OFFSET 5 LIMIT 1)),
    ('Janusz','python','Niebezpieczny drapieżnik', (SELECT id FROM public.shelter OFFSET 0 LIMIT 1)),
    ('Max','dog','Lubi się bawić', (SELECT id FROM public.shelter OFFSET 2 LIMIT 1)),
    ('Filemon','cat','Leniwy, cały dzień śpi', (SELECT id FROM public.shelter OFFSET 1 LIMIT 1)),
    ('Robert','guinea_pig','Szybko biega', (SELECT id FROM public.shelter OFFSET 3 LIMIT 1)),
    ('Bajkał','dog','Bardzo ładne imię', (SELECT id FROM public.shelter OFFSET 2 LIMIT 1)),
    ('Alojzy','guinea_pig','Kolorowa', (SELECT id FROM public.shelter OFFSET 1 LIMIT 1));