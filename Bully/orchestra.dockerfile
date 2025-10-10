# Use latest Python
FROM python:latest

# Set working directory
WORKDIR /app

# Copy both Python files
COPY ["bad_bully.py", "good_bully.py", "./"]

# Create a shell script to run both programs
RUN echo '#!/bin/bash\n\
echo "Running Bad Bully:"\n\
python bad_bully.py\n\
echo "\nRunning Good Bully:"\n\
python good_bully.py' > run.sh

# Make the shell script executable
RUN chmod +x run.sh

# Run the shell script when container starts
CMD ["./run.sh"]
