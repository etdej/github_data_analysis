if __name__ == "__main__":
    import sys
    import grab_data
    import traceback
    import os

    assert len(sys.argv) == 3
    print(sys.argv)
    _, url_file_path, output_base_path = sys.argv
    try:
        with open(url_file_path, "r") as f:
            for url in f.readlines():
                print(url_file_path, url.strip())
                grab_data.download_extract_save(output_base_path, url.strip(),
                                                skip_if_exists=True)
        print(url_file_path, "DONE")
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        with open(os.path.join(output_base_path, "ERROR"), "w") as f:
            f.write(traceback.format_exc())
