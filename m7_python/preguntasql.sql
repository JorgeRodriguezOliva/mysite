select  c.nombre as comuna, i.nombre, i.descripcion from m7_python_inmueble as i join m7_python_comuna as c on c.cod=i.comuna_id where c.nombre ilike '%lum%';

select  r.nombre, i.nombre, i.descripcion from m7_python_inmueble as i join m7_python_comuna as c on c.cod=i.comuna_id join m7_python_region as r on c.region_id=r.cod where r.nombre ilike '%bi%';


select * from m7_python_comuna where nombre ilike '%lu%';      