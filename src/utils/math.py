import numpy as np


def solve_least_squares(A, b):
    x, residuals, _, _ = np.linalg.lstsq(A, b, rcond=None)
    return x, residuals


def solve_least_squares_with_knowns(A, b, known_indices, known_values):
    A_unknown, b_reduced, reconstruct_full = reduce_system_with_knowns(A, b, known_indices, known_values)
    x_unknown, residuals = solve_least_squares(A_unknown, b_reduced)
    x_full = reconstruct_full(x_unknown)
    return x_full, residuals


def reduce_system_with_knowns(A, b, known_indices, known_values):
    order = np.argsort(known_indices)
    known_indices = known_indices[order]
    known_values = known_values[order]
    
    n = A.shape[1]
    mask_known = np.zeros((n,), dtype=bool)
    mask_known[known_indices] = True
    mask_unknown = ~mask_known
    
    A_known = A[:, mask_known]
    A_unknown = A[:, mask_unknown]
    
    b_reduced = b - A_known @ known_values
    
    def reconstruct_full(x_unknown):
        x_full = np.zeros((n,), dtype=float)
        x_full[mask_known] = known_values
        x_full[mask_unknown] = x_unknown
        return x_full
    
    return A_unknown, b_reduced, reconstruct_full
    