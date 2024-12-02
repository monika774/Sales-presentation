import csv
import os

class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Ensure the CSV file exists with correct headers."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=["date", "product", "sales", "region"])
                writer.writeheader()

    def normalize_fields(self, row):
        """Remove trailing/leading spaces from keys."""
        return {key.strip(): value for key, value in row.items()}

    def read_csv(self):
        """Read data from the CSV file."""
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [self.normalize_fields(row) for row in reader]

    def write_csv(self, data):
        """Write data to the CSV file."""
        fieldnames = ["date", "product", "sales", "region"]
        normalized_data = [self.normalize_fields(row) for row in data]
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(normalized_data)
