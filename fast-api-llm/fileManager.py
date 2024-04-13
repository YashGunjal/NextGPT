from llama_index.readers.s3 import S3Reader

class FileManagerS3:
    def __init__(self, aws_access, aws_secret, bucket_name):
        self.access_key = aws_access
        self.secret_key = aws_secret
        self.bucket_name = bucket_name
        

    def get_file(self, file_path):
        """
        Get file content given the S3 file path.
        Returns:
        str: Content of the file if exists, otherwise returns None.
        """
        try:
            reader = S3Reader(aws_access_id=self.access_key ,
                              aws_access_secret=self.secret_key,
                              bucket=self.bucket_name,
                              key=file_path)
            documents = reader.load_s3_files_as_docs()
            return documents
        except TypeError as e:
            print("File not found or not a valid file path.")
            print(f"Error saving data to Store: {e}")


# Example usage:
if __name__ == '__main__':
    file_manager = FileManagerS3()
    file_path = "folder/cf3cf9d5-5369-4c17-9aea-8b54935fcfcc-attention.pdf"  # Change to the path of your file
    file_content = file_manager.get_file(file_path)
    if file_content:
        print("File content:")
        print(file_content)
