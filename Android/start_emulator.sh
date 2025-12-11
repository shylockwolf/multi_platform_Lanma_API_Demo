#!/bin/bash

# Kill all existing emulator processes
echo "Killing all existing emulator processes..."
kill -9 $(pgrep -f "emulator|qemu-system") 2>/dev/null

# Wait for processes to terminate
sleep 3

# Start emulator with explicit window settings
echo "Starting emulator with visible window..."
/Users/noone/Library/Android/sdk/emulator/emulator -avd Medium_Phone_API_36.1 \
    -no-boot-anim \
    -netdelay none \
    -netspeed full &

EMULATOR_PID=$!

# Wait for emulator to boot
echo "Waiting for emulator to boot..."
MAX_WAIT=120
COUNT=0

while true; do
    /Users/noone/Library/Android/sdk/platform-tools/adb devices | grep "emulator-5554\s*device" > /dev/null
    if [ $? -eq 0 ]; then
        echo "Emulator booted successfully!"
        break
    fi
    
    COUNT=$((COUNT+1))
    if [ $COUNT -gt $MAX_WAIT ]; then
        echo "Emulator failed to boot within timeout."
        kill $EMULATOR_PID
        exit 1
    fi
    
    echo "Waiting for emulator... ($COUNT/$MAX_WAIT)"
    sleep 1
done

# Wait a bit more for system to be ready
sleep 5

# Install app
echo "Installing app..."
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
./gradlew installDebug

# Start app
echo "Starting app..."
/Users/noone/Library/Android/sdk/platform-tools/adb shell am start -n com.example.api_demo/.MainActivity

echo "Done! App should be visible in the emulator window."