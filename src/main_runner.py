import src.run_program as gp
import src.get_webcam_open as cp

if __name__ == "__main__":
    try:
        gp.run_gesture_program()
    except KeyboardInterrupt:
        print("Gesture program killed. Launching cursor program...")
    except Exception as e:
        print(f"Gesture program crashed: {e}")
    finally:
        cp.run_cursor_program()