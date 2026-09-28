corr_matrix = df.corr()

# Create a bigger heatmap to reduce clustering
plt.figure(figsize=(18, 14))  # Increase figure size

# Heatmap with adjustments
sns.heatmap(corr_matrix,  
            annot=True,  # Show correlation values
            cmap='coolwarm',  
            fmt=".2f",  # Format numbers
            linewidths=0.5,  # Add lines between cells
            square=True,  # Ensure square cells
            cbar_kws={"shrink": 0.8})  # Adjust color bar size

plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.yticks(rotation=0)  # Keep y-axis labels horizontal
plt.title("Correlation Heatmap of Features", fontsize=16)  # Add title

plt.savefig('correlation_heatmap.png')  # Save the figure as an image
plt.show()