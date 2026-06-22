import sys
import os

try:
    import mosek
    from mosek.fusion import Model, Domain, ObjectiveSense, Expr
except ImportError:
    print("Error: The 'mosek' python package is not installed.")
    print("Please install it using: pip install mosek")
    sys.exit(1)

def verify_mosek():
    print("=========================================")
    print("       MOSEK LICENSE VERIFICATION        ")
    print("=========================================")
    print(f"Hostname:       {os.uname().nodename}")
    print(f"Python:         {sys.version.split()[0]}")
    print(f"Mosek version:  {mosek.Env.getversion()}")
    
    # Check license file environment variable or default path
    env_lic = os.environ.get("MSK_LICENSE_FILE")
    if env_lic:
        print(f"MSK_LICENSE_FILE: {env_lic}")
    else:
        default_path = os.path.expanduser("~/mosek/mosek.lic")
        print("MSK_LICENSE_FILE: [NOT SET] (Using default path)")
        print(f"Checking default path: {default_path}")
        if os.path.exists(default_path):
            print(f"License file exists at default path: Yes")
        else:
            print(f"License file exists at default path: NO")

    try:
        # Solve a tiny linear program to trigger license check and confirm solution logic works
        # Minimize x + y subject to:
        # x + y >= 1.0, x >= 0.0, y >= 0.0
        with Model("MinimalVerification") as M:
            x = M.variable("x", 2, Domain.greaterThan(0.0))
            M.objective("obj", ObjectiveSense.Minimize, Expr.sum(x))
            M.constraint("c", Expr.sum(x), Domain.greaterThan(1.0))
            M.solve()
            
            sol = x.level()
            print(f"Verification solve result: x = {sol[0]:.2f}, y = {sol[1]:.2f}")
            print("MOSEK license is successfully validated on this node!")
            print("=========================================")
    except mosek.Error as e:
        print(f"\nMOSEK error occurred: {e}")
        print("This typically indicates a licensing issue or missing license file.")
        print("=========================================")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error during optimization: {e}")
        print("=========================================")
        sys.exit(1)

if __name__ == "__main__":
    verify_mosek()
