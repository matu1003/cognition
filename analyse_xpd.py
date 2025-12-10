import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def read_xpd(path):
    """
    Reads an Expyriment .xpd file and returns a clean pandas DataFrame.
    Ignores metadata lines starting with '#'.
    """
    df = pd.read_csv(
        path,
        comment="#",        # ignore metadata header
        sep=","
    )
    return df


def analyze_data(df):
    """
    Computes basic descriptive statistics from the XPD dataset.
    Returns a dictionary of results.
    """
    results = {}

    # Reaction time mean and std
    results["RT_mean"] = df["RT"].mean()
    results["RT_std"] = df["RT"].std()

    # Error rate
    results["error_rate"] = 1 - df["correct"].mean()

    # Mean RT by angle
    results["RT_by_angle"] = df.groupby("angle")["RT"].mean()

    # Mean RT by version (normal vs mirror)
    results["RT_by_version"] = df.groupby("version")["RT"].mean()

    # Error rate by angle
    results["errors_by_angle"] = df.groupby("angle")["correct"].apply(lambda x: 1 - x.mean())

    results["accuracy_by_angle"] = df.groupby("angle")["correct"].mean()

    return results


def plot_rt_by_angle(df, savepath="rt_by_angle.png"):
    """Plots RT as a function of rotation angle."""
    plt.figure(figsize=(8,5))
    sns.pointplot(data=df, x="angle", y="RT", errorbar="se")
    plt.title("Reaction Time as a Function of Letter Rotation")
    plt.xlabel("Rotation angle (degrees)")
    plt.ylabel("Reaction Time (ms)")
    plt.grid(True, alpha=0.3)
    plt.savefig(savepath, dpi=300, bbox_inches='tight')
    plt.close()


def plot_rt_by_version(df, savepath="rt_by_version.png"):
    """Plots RT by stimulus condition (normal vs mirror)."""
    plt.figure(figsize=(6,5))
    sns.barplot(data=df, x="version", y="RT", ci=68)
    plt.title("Reaction Time by Condition (Normal vs Mirror)")
    plt.xlabel("Condition")
    plt.ylabel("Reaction Time (ms)")
    plt.grid(True, alpha=0.3)
    plt.savefig(savepath, dpi=300, bbox_inches='tight')
    plt.close()

def plot_accuracy_by_angle(df, savepath="accuracy_by_angle.png"):
    """
    Plots proportion of correct responses as a function of rotation angle.
    """
    plt.figure(figsize=(8, 5))
    sns.pointplot(data=df, x="angle", y="correct", errorbar="se")
    plt.title("Accuracy as a Function of Letter Rotation")
    plt.xlabel("Rotation angle (degrees)")
    plt.ylabel("Proportion correct")
    plt.ylim(0, 1.05)
    plt.grid(True, alpha=0.3)
    plt.savefig(savepath, dpi=300, bbox_inches='tight')
    plt.close()


def main():
    path = "data/base_016.xpd"   # <- change this to your .xpd file path
    df = read_xpd(path)

    print("\n=== BASIC STATS ===")
    results = analyze_data(df)
    for k, v in results.items():
        print(f"{k}: \n{v}\n")

    # Generate plots for the README
    plot_rt_by_angle(df)
    plot_rt_by_version(df)
    plot_accuracy_by_angle(df)

    print("Figures saved: rt_by_angle.png, rt_by_version.png")


if __name__ == "__main__":
    main()
