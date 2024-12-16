import serial
import time
import logging

# 设置日志级别
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_serial_basic():
    """基本的串口通信测试"""
    try:
        # 连接串口
        port = "COM11"  # 使用实际的端口号
        ser = serial.Serial(
            port=port,
            baudrate=115200,
            timeout=2.0
        )
        logger.info(f"Connected to {port}")

        # 测试发送命令并接收响应
        commands = [
            "PICO_INFO\r\n",  # 添加换行符
            "PWM 50\r\n"
        ]

        for cmd in commands:
            logger.info(f"\nTesting command: {cmd.strip()}")
            
            # 清空缓冲区
            ser.reset_input_buffer()
            ser.reset_output_buffer()
            
            # 发送命令
            bytes_written = ser.write(cmd.encode())
            logger.info(f"Sent {bytes_written} bytes")
            ser.flush()
            
            # 等待一段时间确保命令被处理
            time.sleep(0.1)
            
            # 读取响应
            while ser.in_waiting:
                response = ser.readline()
                try:
                    decoded = response.decode().strip()
                    logger.info(f"Raw response: {response}")
                    logger.info(f"Decoded response: {decoded}")
                except UnicodeDecodeError:
                    logger.error(f"Failed to decode response: {response}")
                
                # 如果收到完整响应就退出
                if decoded.startswith("OK") or "ERROR" in decoded:
                    break
            
            time.sleep(1)  # 命令之间等待
            
        ser.close()
        logger.info("Test completed successfully")
        
    except serial.SerialException as e:
        logger.error(f"Serial error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    test_serial_basic()
