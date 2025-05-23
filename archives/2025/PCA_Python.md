---
title: How PCA Components Are Linearly Decomposed?
number: 1
link: '/archives/2025/PCA_Python.md'
created_at: '2025-05-15 13:07:27'
updated_at: '2025-05-15 14:55:04'
labels:
  - documentation
---

# How PCA Components Are Linearly Decomposed

One of the most important things to understand about PCA is this:

Each principal component is a linear combination of the original features.

That means:

- PCA doesn't just pick some features and discard others.

It creates new features (components) by mixing the original ones together using weights (called loadings).

The Math Behind It

Let’s suppose we have:
An original dataset X with shape (n_samples, n_features)
PCA returns:
Principal components (i.e., directions in feature space) → components_array of shape (n_components, n_features)
Transformed data → X_transformed = dot product of centered X and components

Let's See It in Code
Let’s go back to the example:

```python
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Create the dataset
X = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# Always standardize before PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)
X_transformed = pca.fit_transform(X_scaled)

# Print principal components (directions)
print("Principal Components (eigenvectors):")
print(pca.components_)

# Print explained variance
print("\nExplained Variance Ratio:")
print(pca.explained_variance_ratio_)

# Print transformed data (projections)
print("\nTransformed Data (X_transformed):")
print(X_transformed)
```

Output:
Let’s break it down step by step. Here's what you’ll see (values may vary slightly):

Principal Components (eigenvectors):

```
[[ 0.57735027  0.57735027  0.57735027]
 [-0.81649658  0.40824829  0.40824829]]
```

Explained Variance Ratio:

```
[1.00000000e+00 5.55111512e-17]
```

Transformed Data (X_transformed):

```
[[ 2.12132034e+00  1.66533454e-16]
 [ 0.00000000e+00 -3.33066907e-16]
 [-2.12132034e+00  1.66533454e-16]]
 ```

What Does This Mean?

1. Principal Components = Linear Combinations
Each row of pca.components_ is a unit vector (length = 1) that defines one principal component. Each component tells you how much each original feature contributes.

For example, the first principal component:

```
[0.577, 0.577, 0.577]
```

Means:

PC1 = 0.577*x1 + 0.577*x2 + 0.577*x3
This component gives equal weight to all three features.

The second component:

```
[-0.816, 0.408, 0.408]
```

Means:

PC2 = -0.816*x1 + 0.408*x2 + 0.408*x3
This tries to cancel out x1 while combining x2 and x3 positively.

2. Transformed Data = Projection Onto Components
Each row in X_transformed is the original data point projected onto the component axes. In linear algebra terms:

X_transformed = X_scaled · components_.T
So the first row of transformed data:

[2.121, 0.000]
means that the first sample lies strongly in the direction of PC1 and nearly zero in the direction of PC2.

3. Reconstructing Original Data
You can even reverse the transformation (approximate reconstruction):

X_reconstructed = pca.inverse_transform(X_transformed)
print("\nReconstructed Data (approximation):")
print(X_reconstructed)
Output (very close to standardized data):

```
[[-1.2247, -1.2247, -1.2247],
 [ 0.0000,  0.0000,  0.0000],
 [ 1.2247,  1.2247,  1.2247]]
 ```

This confirms that we’ve just rotated and projected the original data.

Summary of PCA Decomposition
Term Meaning
Principal Component A new feature formed as a linear combination of the original ones
Weights (Loadings) Coefficients in the linear combination
Projection Dot product of centered data with the component vector
Explained Variance How much of the data’s spread is captured by each component
Visualization Tip
If you want to visualize the importance of each feature in each principal component, try this:

import pandas as pd
import matplotlib.pyplot as plt

## Create a DataFrame for easy plotting

```
components_df = pd.DataFrame(pca.components_, columns=['x1', 'x2', 'x3'], index=['PC1', 'PC2'])
components_df.T.plot(kind='bar')
plt.title("Feature Weights in Each Principal Component")
plt.ylabel("Weight")
plt.grid(True)
plt.show()
```

This will give you a bar chart showing how much each feature contributes to PC1 and PC2.

Final Takeaway
PCA is more than a black-box dimensionality reduction tool—it’s a coordinate transformation that reveals new directions (principal axes) in your data where variance is maximized. By understanding the weights of each component, you gain powerful insights into the structure of your data and how features interact.
