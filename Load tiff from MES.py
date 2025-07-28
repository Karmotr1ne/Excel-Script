import hdf5plugin
import h5py
import numpy as np
import tifffile
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def read_zlevel(f, df):
    ds = f[f'{df}/Zlevel']
    raw = ds[()]

    if isinstance(raw, h5py.Reference):
        arr = f[raw][()]
    elif isinstance(raw, np.ndarray) and raw.dtype == object:
        ref = raw.flat[0]
        arr = f[ref][()]
    else:
        arr = raw

    if np.isscalar(arr):
        return float(arr)
    else:
        return float(np.array(arr).flat[0])


def main():
    # Hide root window
    root = Tk()
    root.withdraw()

    # Prompt user to select MES file
    mes_file = askopenfilename(
        title="Select MES file",
        filetypes=[('MES files', '*.mes'), ('All files', '*.*')]
    )
    if not mes_file:
        print("No MES file selected, exiting.")
        return

    # Prompt user to choose output TIFF path
    output_tiff = asksaveasfilename(
        title="Save output TIFF as",
        defaultextension='.tiff',
        filetypes=[('TIFF files', '*.tiff'), ('All files', '*.*')]
    )
    if not output_tiff:
        print("No output file specified, exiting.")
        return

    images = []
    z_levels = []

    with h5py.File(mes_file, 'r') as f:
        # Collect image groups sorted by stage and frame
        img_keys = sorted(
            [k for k in f.keys() if k.startswith('IF') and '_' in k],
            key=lambda x: (int(x[2:6]), int(x.split('_')[1]))
        )

        for key in img_keys:
            img = f[key][:]
            if img.size == 0:
                continue

            df = 'DF' + key[2:6]
            try:
                z = read_zlevel(f, df)
            except Exception as e:
                print(f'Fail to read {df}: {e}')
                continue

            images.append(img)
            z_levels.append(z)

    if not images:
        print("No images found in the MES file.")
        return

    # Pad images to same shape
    shapes = [im.shape for im in images]
    max_h, max_w = max(h for h, w in shapes), max(w for h, w in shapes)
    padded = []
    for im in images:
        h, w = im.shape
        pad_h = max_h - h
        pad_w = max_w - w
        padded.append(
            np.pad(im,
                   ((0, pad_h), (0, pad_w)),
                   mode='constant', constant_values=0)
        )

    # Build z-stack
    stack = np.stack(padded, axis=0)  # (N, H, W)
    z_arr = np.array(z_levels)
    order = np.argsort(z_arr)
    zstack = stack[order]

    # Save as TIFF
    tifffile.imwrite(
        output_tiff,
        zstack.astype(np.uint16),
        imagej=True,
        metadata={
            'spacing': float(np.diff(z_arr[order]).mean()),
            'unit': 'um'
        }
    )
    print(f'Saved {zstack.shape[0]} layers to {output_tiff}')


if __name__ == '__main__':
    main()