ALTER TABLE IF EXISTS ONLY public.user_table DROP CONSTRAINT IF EXISTS pk_user_table_id CASCADE;


DROP TABLE IF EXISTS public.user_table;
DROP SEQUENCE IF EXISTS public.user_table_id_seq;
CREATE TABLE user_table (
    id serial NOT NULL,
    user_name varchar UNIQUE,
    password varchar
);


ALTER TABLE ONLY user_table
    ADD CONSTRAINT pk_user_table_id PRIMARY KEY (id);