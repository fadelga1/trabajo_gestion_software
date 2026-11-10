# Estructura de Base de Datos — SIGR

**Motor:** SQLite 3
**Archivo:** `instance/sigr.db`
**ORM:** Flask-SQLAlchemy 3.1.1

## Tablas

### `usuarios`
| Campo | Tipo | Restricción |
|---|---|---|
| id | Integer | PK, autoincrement |
| nombre | String(80) | NOT NULL |
| email | String(120) | UNIQUE, NOT NULL |
| password_hash | String(200) | NOT NULL |
| rol | String(20) | NOT NULL (`admin`, `mesero`, `cliente`) |

### `categorias`
| Campo | Tipo | Restricción |
|---|---|---|
| id | Integer | PK |
| nombre | String(80) | UNIQUE, NOT NULL |

### `platos`
| Campo | Tipo | Restricción |
|---|---|---|
| id | Integer | PK |
| nombre | String(120) | NOT NULL |
| descripcion | String(255) | — |
| precio | Float | NOT NULL |
| disponible | Boolean | default True |
| categoria_id | Integer | FK → categorias.id |

### `pedidos`
| Campo | Tipo | Restricción |
|---|---|---|
| id | Integer | PK |
| fecha | DateTime | default now() |
| estado | String(20) | (`pendiente`, `preparando`, `listo`, `entregado`, `pagado`) |
| cliente_id | Integer | FK → usuarios.id |
| mesero_id | Integer | FK → usuarios.id |
| total | Float | default 0.0 |

### `items_pedido`
| Campo | Tipo | Restricción |
|---|---|---|
| id | Integer | PK |
| pedido_id | Integer | FK → pedidos.id |
| plato_id | Integer | FK → platos.id |
| cantidad | Integer | default 1 |
| precio_unitario | Float | NOT NULL |

### `reservas`
| Campo | Tipo | Restricción |
|---|---|---|
| id | Integer | PK |
| cliente_id | Integer | FK → usuarios.id |
| fecha | Date | NOT NULL |
| hora | Time | NOT NULL |
| personas | Integer | NOT NULL |
| estado | String(20) | default `activa` |

### `cierres_caja`
| Campo | Tipo | Restricción |
|---|---|---|
| id | Integer | PK |
| fecha | Date | UNIQUE (implícito por lógica) |
| total_ventas | Float | default 0.0 |
| num_pedidos | Integer | default 0 |
| hora_cierre | DateTime | default now() |

## Relaciones
- `Categoria` 1—N `Plato`
- `Pedido` 1—N `ItemPedido`
- `Pedido` N—1 `Usuario` (cliente y mesero)
- `Reserva` N—1 `Usuario` (cliente)

## Diagrama


## Credenciales demo
| Rol | Email | Password |
|---|---|---|
| Admin | admin@sigr.com | admin123 |
| Mesero | mesero@sigr.com | mesero123 |
| Cliente | cliente@sigr.com | cliente123 |
