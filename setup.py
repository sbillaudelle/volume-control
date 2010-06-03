from cream.dist import setup

setup('src/manifest.xml',
    data_files = [
        ('{module_dir}', ['src/volume.py', 'src/manifest.xml'])
        ]
    )
