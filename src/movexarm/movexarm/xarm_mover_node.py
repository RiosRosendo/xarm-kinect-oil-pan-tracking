#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from xarm_msgs.srv import MoveCartesian, SetInt16ById, SetInt16


class XArmMoverNode(Node):
    def __init__(self):
        super().__init__('xarm_mover_node')
        
        # Clientes de servicios
        self.move_client = self.create_client(MoveCartesian, '/xarm/set_position')
        self.motion_enable_client = self.create_client(SetInt16ById, '/xarm/motion_enable')
        self.set_state_client = self.create_client(SetInt16, '/xarm/set_state')
        
        # Esperar a que los servicios estén disponibles
        self.wait_for_services()
        
        self.get_logger().info('Nodo XArm Mover iniciado')
        
        # Habilitar el xArm y luego mover
        self.enable_and_move()
    
    def wait_for_services(self):
        """Espera a que todos los servicios estén disponibles"""
        services = [
            (self.move_client, '/xarm/set_position'),
            (self.motion_enable_client, '/xarm/motion_enable'),
            (self.set_state_client, '/xarm/set_state')
        ]
        
        for client, service_name in services:
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f'Esperando el servicio {service_name}...')
    
    def enable_xarm(self):
        """Habilita el xArm usando los servicios necesarios"""
        # 1. Habilitar movimiento
        self.get_logger().info('Habilitando movimiento del xArm...')
        motion_request = SetInt16ById.Request()
        motion_request.id = 8  # ID para motion enable
        motion_request.data = 1  # 1 para habilitar, 0 para deshabilitar
        
        try:
            future = self.motion_enable_client.call_async(motion_request)
            rclpy.spin_until_future_complete(self, future)
            response = future.result()
            
            if response.ret == 0:
                self.get_logger().info('Movimiento habilitado exitosamente')
            else:
                self.get_logger().error(f'Error habilitando movimiento. Código: {response.ret}')
                return False
        except Exception as e:
            self.get_logger().error(f'Error llamando motion_enable: {str(e)}')
            return False
        
        # 2. Establecer estado operativo
        self.get_logger().info('Estableciendo estado operativo...')
        state_request = SetInt16.Request()
        state_request.data = 0  # Estado operativo
        
        try:
            future = self.set_state_client.call_async(state_request)
            rclpy.spin_until_future_complete(self, future)
            response = future.result()
            
            if response.ret == 0:
                self.get_logger().info('Estado operativo establecido exitosamente')
                return True
            else:
                self.get_logger().error(f'Error estableciendo estado. Código: {response.ret}')
                return False
        except Exception as e:
            self.get_logger().error(f'Error llamando set_state: {str(e)}')
            return False
    
    def enable_and_move(self):
        """Habilita el xArm y luego ejecuta el movimiento"""
        if self.enable_xarm():
            # Esperar un momento antes de moverse
            import time
            time.sleep(1.0)
            self.move_to_position()
        else:
            self.get_logger().error('No se pudo habilitar el xArm. Cancelando movimiento.')
    
    def move_to_position(self):
        """
        Mueve el xArm a la posición especificada usando el servicio ROS2
        """
        # Crear la petición del servicio
        request = MoveCartesian.Request()
        
        # Configurar la pose: [x, y, z, roll, pitch, yaw]
        # Posición: x=169mm, y=0mm, z=400mm
        # Orientación: roll=3.14rad, pitch=0rad, yaw=0rad
        request.pose = [169.0, 0.0, 400.0, 3.14, 0.0, 0.0]
        request.speed = 30.0
        
        self.get_logger().info(f'Enviando petición para mover a posición: {request.pose}')
        self.get_logger().info(f'Velocidad: {request.speed}')
        
        # Enviar la petición de forma asíncrona
        future = self.move_client.call_async(request)
        future.add_done_callback(self.service_callback)
    
    def service_callback(self, future):
        """
        Callback que se ejecuta cuando el servicio responde
        """
        try:
            response = future.result()
            if response.ret == 0:
                self.get_logger().info('¡Movimiento exitoso!')
            else:
                self.get_logger().error(f'Error en el movimiento. Código: {response.ret}')
        except Exception as e:
            self.get_logger().error(f'Error llamando al servicio: {str(e)}')


def main(args=None):
    rclpy.init(args=args)
    
    # Crear el nodo
    node = XArmMoverNode()
    
    try:
        # Mantener el nodo activo
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # Limpiar recursos
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main() 