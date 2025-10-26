import time
import traceback

import src.run_program as gp
import src.get_webcam_open as cp

def run_gesture():
    gp.run_gesture_program()

def run_cursor():
    cp.run_cursor_program()

if __name__ == "__main__":
    # Start with gp, flip after each termination (normal or crash)
    run_gp_next = True
    backoff_sec = 0.5
    while True:
        if run_gp_next:
            name, fn = "Gesture Program (gp)", run_gesture
        else:
            name, fn = "Cursor Program (cp)", run_cursor

        print(f"[launcher] Starting {name}...")
        try:
            fn()
            print(f"[launcher] {name} exited normally.")
        except KeyboardInterrupt:
            print(f"[launcher] {name} interrupted by user (KeyboardInterrupt).")
        except Exception as e:
            # Log the crash and keep going by switching to the other program
            print(f"[launcher] {name} crashed: {e}")
            traceback.print_exc()


        run_gp_next = not run_gp_next

        # Brief backoff so we don't hammer the CPU if one process fails instantly
        time.sleep(backoff_sec)