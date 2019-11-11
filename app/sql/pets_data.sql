INSERT INTO
    public.pet (pet_name,pet_type,description,shelter_id)
VALUES
    ('Kulfon','dog','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('Azor','dog','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('Burek','dog','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('Tadeusz','cat','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('Max','sds','parrot', (SELECT id FROM public.shelter LIMIT 1)),
    ('dfs','sds','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('dfs','sds','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('dfs','sds','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('dfs','sds','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('dfs','sds','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('dfs','sds','dddd', (SELECT id FROM public.shelter LIMIT 1)),
    ('dfs','sds','dddd', (SELECT id FROM public.shelter LIMIT 1));