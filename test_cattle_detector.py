from pathlib import Path
from backend.cattle_detector import detect_cattle


def main():

    print("\n======================================")
    print("       CATTLE DETECTION TEST")
    print("======================================")

    # Ask user for image path
    image_path = input("\nEnter image path: ").strip().strip('"')

    # Validate image path
    path = Path(image_path)

    if not path.exists():
        print("\nERROR: Image file not found!")
        return

    if not path.is_file():
        print("\nERROR: The provided path is not a file!")
        return

    try:

        # Read image
        with open(path, "rb") as file:
            image_bytes = file.read()

        print("\nAnalyzing image...")

        # Run cattle detection
        result = detect_cattle(image_bytes)

        print("\n======================================")
        print("          DETECTION RESULT")
        print("======================================")

        if result["cattle_detected"]:

            print("\nCATTLE DETECTED!")

            for index, detection in enumerate(
                result["detections"], start=1
            ):

                print(f"\nDetection {index}")
                print("Class:", detection["class"])
                print("Confidence:", detection["confidence"], "%")
                print("Bounding Box:", detection["box"])

        else:

            print("\nNO CATTLE DETECTED!")
            print("This image cannot proceed to breed identification.")

        print("\n======================================")

    except Exception as error:
        print("\nDetection failed:", str(error))


if __name__ == "__main__":
    main()