#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from xarm_msgs.srv import MoveCartesian, SetInt16ById, SetInt16
import sys


class XArmInteractiveMover(Node):
    def __init__(self):
        super().__init__('xarm_interactive_mover')
        
        # Clientes de servicios
        self.move_client = self.create_client(MoveCartesian, '/xarm/set_position')
        self.motion_enable_client = self.create_client(SetInt16ById, '/xarm/motion_enable')
        self.set_state_client = self.create_client(SetInt16, '/xarm/set_state')
        
        # Esperar a que los servicios estén disponibles
        self.wait_for_services()
        
        self.get_logger().info('Nodo XArm Interactive Mover iniciado')
        
        # Habilitar el xArm al iniciar
        self.enable_xarm()
    
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
    
    def move_to_position(self, x, y, z, roll, pitch, yaw, speed=30.0):
        """
        Mueve el xArm a la posición especificada
        
        Args:
            x, y, z: Posición cartesiana en mm
            roll, pitch, yaw: Orientación en radianes
            speed: Velocidad del movimiento
        """
        # Crear la petición del servicio
        request = MoveCartesian.Request()
        request.pose = [float(x), float(y), float(z), float(roll), float(pitch), float(yaw)]
        request.speed = float(speed)
        
        self.get_logger().info(f'Enviando petición para mover a posición:')
        self.get_logger().info(f'  Posición: x={x}mm, y={y}mm, z={z}mm')
        self.get_logger().info(f'  Orientación: roll={roll}rad, pitch={pitch}rad, yaw={yaw}rad')
        self.get_logger().info(f'  Velocidad: {speed}')
        
        # Enviar la petición de forma síncrona
        try:
            future = self.move_client.call_async(request)
            rclpy.spin_until_future_complete(self, future)
            response = future.result()
            
            if response.ret == 0:
                self.get_logger().info('¡Movimiento exitoso!')
                return True
            else:
                self.get_logger().error(f'Error en el movimiento. Código: {response.ret}')
                return False
        except Exception as e:
            self.get_logger().error(f'Error llamando al servicio: {str(e)}')
            return False
    
    def move_to_predefined_positions(self):
        """
        Mueve el xArm a posiciones predefinidas
        """
        positions = [
            # Posición inicial
            {"name": "Posición inicial", "x": 169, "y": 0, "z": 400, "roll": 3.14, "pitch": 0, "yaw": 0},
            # Posición lateral
            {"name": "Posición lateral", "x": 200, "y": 150, "z": 450, "roll": 3.14, "pitch": 0, "yaw": 0.5},
            # Posición elevada
            {"name": "Posición elevada", "x": 169, "y": 0, "z": 500, "roll": 3.14, "pitch": 0, "yaw": 0},
        ]
        
        for pos in positions:
            self.get_logger().info(f'Moviendo a: {pos["name"]}')
            success = self.move_to_position(
                pos["x"], pos["y"], pos["z"], 
                pos["roll"], pos["pitch"], pos["yaw"]
            )
            
            if success:
                # Esperar un poco entre movimientos
                import time
                time.sleep(2.0)
            else:
                self.get_logger().error(f'Falló el movimiento a {pos["name"]}')
                break


def main(args=None):
    rclpy.init(args=args)
    
    # Crear el nodo
    node = XArmInteractiveMover()
    
    try:
        # Verificar argumentos de línea de comandos
        if len(sys.argv) >= 7:
            # Modo con parámetros específicos
            x = float(sys.argv[1])
            y = float(sys.argv[2])
            z = float(sys.argv[3])
            roll = float(sys.argv[4])
            pitch = float(sys.argv[5])
            yaw = float(sys.argv[6])
            speed = float(sys.argv[7]) if len(sys.argv) > 7 else 30.0
            
            node.move_to_position(x, y, z, roll, pitch, yaw, speed)
        else:
            # Modo predefinido
            node.get_logger().info('Ejecutando secuencia de movimientos predefinidos...')
            node.move_to_predefined_positions()
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        node.get_logger().error(f'Error: {str(e)}')
    finally:
        # Limpiar recursos
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main() 