import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Create figures directory if it doesn't exist
Path('figures').mkdir(parents=True, exist_ok=True)

# 1. Load Data
df = pd.read_csv('metrics/results/metric_scores.csv')

# Define language groups
high_res = ['de', 'fr', 'zh', 'es', 'ja']
low_res = ['hi', 'ar', 'bn', 'mr', 'pa', 'ta', 'te']

# Map languages to resource levels
def get_resource_level(lang):
    if lang in high_res:
        return 'High-Resource (5 pairs)'
    elif lang in low_res:
        return 'Low-Resource (7 pairs)'
    return 'Unknown'

df['Resource Level'] = df['lang'].apply(get_resource_level)

# 2. Figure 1: COMET by System
# Group and calculate means
comet_means = df.groupby(['system', 'Resource Level'])['comet'].mean().reset_index()

# Sort systems for better visualization
system_order = ['google_translate', 'microsoft_translator', 'nllb200', 'madlad400', 'indictrans2']
comet_means['system'] = pd.Categorical(comet_means['system'], categories=system_order, ordered=True)
comet_means = comet_means.sort_values('system')

plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")
ax = sns.barplot(
    data=comet_means, 
    x='system', 
    y='comet', 
    hue='Resource Level',
    palette='Set2'
)
plt.title('Mean COMET Score by System and Resource Level', pad=15, fontsize=14)
plt.ylabel('COMET Score', fontsize=12)
plt.xlabel('NMT System', fontsize=12)
plt.ylim(0.75, 0.95)  # Zoom in on the relevant variance range
plt.xticks(rotation=15)
plt.legend(title='Category', loc='lower right')
plt.tight_layout()
plt.savefig('figures/comet_by_system.png', dpi=300)
plt.close()
print("Generated figures/comet_by_system.png")

# 3. Figure 2: Metric Correlation Heatmap
# Invert TER so that higher is better (aligns positively with other metrics)
df_corr = df.copy()
df_corr['ter_inverted'] = -df_corr['ter']

# Select metrics for correlation
metrics = ['bleu', 'meteor', 'chrf', 'rouge_l', 'ter_inverted', 'comet', 'bertscore']
corr_matrix = df_corr[metrics].corr(method='kendall')

# Rename labels for a cleaner plot
labels = ['BLEU', 'METEOR', 'chrF++', 'ROUGE-L', 'TER (inv)', 'COMET', 'BERTScore']
corr_matrix.columns = labels
corr_matrix.index = labels

plt.figure(figsize=(8, 6))
sns.heatmap(
    corr_matrix, 
    annot=True, 
    cmap='coolwarm', 
    vmin=0, 
    vmax=1, 
    fmt=".2f",
    square=True,
    cbar_kws={"shrink": .8}
)
plt.title("Kendall's Tau Rank Correlation Among Metrics", pad=15, fontsize=14)
plt.tight_layout()
plt.savefig('figures/metric_correlation.png', dpi=300)
plt.close()
print("Generated figures/metric_correlation.png")
