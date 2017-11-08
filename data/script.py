if __name__ == "__main__":
    import sys
    import grab_data

    assert len(sys.argv) == 3
    _, url_file_path, output_base_path = sys.argv
    with open(url_file_path, "r") as f:
        for url in f.readlines():
            grab_data.download_extract_save(output_base_path, url)

