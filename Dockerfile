FROM python:3.11-slim

WORKDIR /app

# Install the mosek library required by the python code under test
RUN pip install --no-cache-dir mosek

# Copy the script and unit tests
COPY solve.py test_solve.py ./

# Run the test suite on container startup
CMD ["python", "-m", "unittest", "test_solve.py"]
