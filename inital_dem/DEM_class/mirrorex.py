import numpy as np

def mirror_and_rotate_array(arr):
    if arr.size == 0:
        return arr

    num_rows, num_cols = arr.shape

    # Create a new larger array with mirrored values
    mirrored_arr = np.zeros((num_rows * 2, num_cols * 2), dtype=arr.dtype)

    # Mirror the original array into the center of the new array
    mirrored_arr[num_rows:2*num_rows, num_cols:2*num_cols] = arr

    # Mirror and rotate the corners
    mirrored_arr[:num_rows, :num_cols] = np.rot90(np.flipud(arr), k=2)  # Top-left corner
    mirrored_arr[:num_rows, 2*num_cols:] = np.rot90(np.flipud(arr), k=1)  # Top-right corner
    mirrored_arr[2*num_rows:, :num_cols] = np.rot90(np.flipud(arr), k=3)  # Bottom-left corner
    mirrored_arr[2*num_rows:, 2*num_cols:] = np.rot90(np.flipud(arr))  # Bottom-right corner

    return mirrored_arr

# Example usage:
original_array = np.array([
    [1, 2],
    [3, 4]
])

mirrored_result = mirror_and_rotate_array(original_array)
print(mirrored_result)
