import os
import shutil
import random
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train')
    val_data_path: str = os.path.join('artifacts', 'Validation')
    test_data_path: str = os.path.join('artifacts', 'Test')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered data ingestion component")

        root_dir = 'notebook/Osteosarcoma-UT_data'

        logging.info("Got the root directory of dataset")

        os.makedirs(self.ingestion_config.train_data_path, exist_ok=True)
        os.makedirs(self.ingestion_config.val_data_path, exist_ok=True)
        os.makedirs(self.ingestion_config.test_data_path, exist_ok=True)

        classes = os.listdir(root_dir)

        try:
            for class_name in classes:
                class_dir = os.path.join(root_dir, class_name)
                images = os.listdir(class_dir)
                random.shuffle(images)  # Shuffle images to split randomly

                logging.info(f"There are {len(images)} images belong to {class_name} class")

                train_images, val_images, test_images = self.split_images(images)

                logging.info(f"For class `{class_name}` there are {len(train_images)} train images, {len(val_images)} validation images, {len(test_images)} test images")
                logging.info("-----------------------")

                self.move_images(train_images, class_name,root_dir, self.ingestion_config.train_data_path)
                self.move_images(val_images, class_name,root_dir, self.ingestion_config.val_data_path)
                self.move_images(test_images, class_name,root_dir, self.ingestion_config.test_data_path)

            logging.info("Data ingestion completed successfully.")
        except Exception as e:
            logging.error("Error occurred during data ingestion:", e)
            raise CustomException(e)

    def split_images(self, images, train_ratio=0.7, test_ratio=0.15, val_ratio=0.15):
        num_images = len(images)
        train_split = int(num_images * train_ratio)
        val_split = int(num_images * (test_ratio + val_ratio))

        train_images = images[:train_split]
        val_images = images[train_split:train_split + (val_split // 2)]
        test_images = images[train_split + (val_split // 2):]

        return train_images, val_images, test_images

    def move_images(self, images, class_name,root_dir, destination_dir):
        for img in images:
            src = os.path.join(root_dir, class_name, img)
            dst = os.path.join(destination_dir, class_name, img)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)

if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
