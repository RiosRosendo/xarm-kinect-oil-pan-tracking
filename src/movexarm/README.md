# Paquete MovexArm

Este paquete ROS2 proporciona nodos para controlar el robot xArm6 usando servicios ROS2.

## Funcionalidades

El paquete incluye dos nodos principales:

1. **xarm_mover_node**: Nodo básico que habilita el xArm y lo mueve a una posición predefinida
2. **xarm_interactive_mover**: Nodo interactivo que permite especificar posiciones personalizadas

## Dependencias

- `rclpy`
- `xarm_msgs`

## Instalación

1. Compilar el paquete:
```bash
cd /path/to/your/ros2_ws
colcon build --packages-select movexarm
source install/setup.bash
```

## Uso

### Servicios utilizados

Los nodos automáticamente llaman a estos servicios para habilitar el xArm:

- `/xarm/motion_enable` - Habilita el movimiento del robot
- `/xarm/set_state` - Establece el estado operativo (0)
- `/xarm/set_position` - Mueve el robot a la posición especificada

### Nodo básico (xarm_mover_node)

Ejecuta el nodo que mueve el xArm a la posición [169, 0, 400, 3.14, 0, 0]:

```bash
ros2 run movexarm xarm_mover_node
```

### Nodo interactivo (xarm_interactive_mover)

#### Modo automático (posiciones predefinidas):
```bash
ros2 run movexarm xarm_interactive_mover
```

#### Modo manual (posición específica):
```bash
ros2 run movexarm xarm_interactive_mover <x> <y> <z> <roll> <pitch> <yaw> [velocidad]
```

Ejemplo:
```bash
ros2 run movexarm xarm_interactive_mover 169 0 400 3.14 0 0 30.0
```

## Parámetros

- **x, y, z**: Posición cartesiana en milímetros
- **roll, pitch, yaw**: Orientación en radianes
- **velocidad**: Velocidad del movimiento (opcional, por defecto 30.0)

## Equivalencia con comandos de servicio

El nodo hace el equivalente de ejecutar estos comandos:

```bash
# Habilitar movimiento
ros2 service call /xarm/motion_enable xarm_msgs/srv/SetBool "{data: true}"

# Establecer estado operativo
ros2 service call /xarm/set_state xarm_msgs/srv/SetInt16 "{data: 0}"

# Mover a posición
ros2 service call /xarm/set_position xarm_msgs/srv/MoveCartesian "pose: [169, 0, 400, 3.14, 0, 0], speed: 30.0"
```

## Notas

- El nodo automáticamente habilita el xArm antes de ejecutar cualquier movimiento
- Los movimientos son síncronos para garantizar que se completen antes de continuar
- Se incluye manejo de errores y logging detallado 