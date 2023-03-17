CREATE TABLE IF NOT EXISTS public.Classification
(
    ID character(1) NOT NULL,
    Name character varying,
    CONSTRAINT Classification_pkey PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS public.Category
(
    ID character varying(4) NOT NULL,
    Name character varying,
    ClassificationID character(1),
    CONSTRAINT catergory_pkey PRIMARY KEY (ID),
    CONSTRAINT classification_id_to_category FOREIGN KEY (ClassificationID)
        REFERENCES public.classification (ID) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.Sub_category
(
    ID character(4) NOT NULL,
    Name character varying,
    CategoryID character(4),
    CONSTRAINT SubCategory_pkey PRIMARY KEY (ID),
    CONSTRAINT category_id_to_subcategory FOREIGN KEY (CategoryID)
        REFERENCES public.Category (ID) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE IF NOT EXISTS public.Items
(
    ID serial NOT NULL,
    Name character varying,
    tname character varying,
    Description character varying,
    Price numeric,
    CategoryID character(4),
    SubCatID character(4),
    ClassificationID character(1) NOT NULL,
    Img_url character varying,
    CONSTRAINT Items_pkey PRIMARY KEY (ID),
    CONSTRAINT category_id_to_items FOREIGN KEY (CategoryID)
        REFERENCES public.Category (ID) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT classification_id_to_items FOREIGN KEY (ClassificationID)
        REFERENCES public.Classification (ID) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT subcategory_id_to_items FOREIGN KEY (SubCatID)
        REFERENCES public.Sub_category (ID) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);
