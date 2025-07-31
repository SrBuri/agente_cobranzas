-- Tabla principal de clientes
create table clientes (
    id_cliente serial primary key  not NULL,
    nombre text not null,
    contrato text unique not null,
    segmento text check (segmento in ('Cobro', 'Descuento', 'Convenio')) not null,
    facturas_vencidas integer not null,
    monto_deuda numeric(10,2) not null,
    direccion text,
    referencias text,
    telefono1 text,
    telefono2 text,
    tipo_cliente text check (tipo_cliente in ('Titular', 'Tercero encargado', 'Tercero no encargado')) default 'Titular',
    estado text check (estado in ('Pendiente', 'Gestionado', 'Compromiso', 'No contactado')) default 'Pendiente',
    observaciones text,
    activo boolean default True,
    updated_at timestamp default now()
);

-- Tabla de gestiones realizadas (historial de llamadas o contactos)
create table gestiones (
    id serial primary key,
    cliente_id integer references clientes(id_cliente) on delete cascade,
    fecha_llamada timestamp default now(),
    canal_contacto text check (canal_contacto in ('Teléfono', 'WhatsApp', 'Otro')),
    resultado text,
    resumen text,
    ejecutivo text,
    activo boolean default True,
    updated_at timestamp default now()
);

-- Tabla de compromisos de pago registrados
create table compromisos_pago (
    id serial primary key,
    cliente_id integer references clientes(id_cliente) on delete cascade,
    monto_acordado numeric(10,2) not null,
    fecha_pago date not null,
    canal_pago text,
    estado text check (estado in ('Pendiente', 'Cumplido', 'Incumplido')) default 'Pendiente',
    activo boolean default True,
    updated_at timestamp default now()
);

-- Tabla de objeciones registradas por los clientes
create table objeciones_cliente (
    id serial primary key,
    cliente_id integer references clientes(id_cliente) on delete cascade,
    tipo_objecion text check (tipo_objecion in (
        'Falta de dinero',
        'Confusión sobre factura',
        'Titular fallecido',
        'No vive en el predio',
        'Problemas de salud',
        'Resistencia al pago'
    )),
    mensaje text,
    fecha timestamp default now(),
    activo boolean default True,
    updated_at timestamp default now()
);
