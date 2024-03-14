import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway, bartlett, shapiro, chi2_contingency, kruskal

import warnings
#import warnings


emotion_fields = {
    "emotion_1": "Happy or delightful",
    "emotion_2": "Amusing or funny",
    "emotion_3": "Beauty or liking",
    "emotion_4": "Calm or relaxing",
    "emotion_5": "Energizing or invigorating",
    "emotion_6": "Angry or aggressive",
    "emotion_7": "Triumphant or awe-inspiring",
}

renamed_emotions = {k: v.split(" ")[0] for k, v in emotion_fields.items()}

for k_old, k_new in renamed_emotions.items():
    emotion_fields[k_new] = emotion_fields.pop(k_old)

music_perceptual_features = {
    "feature_1": ("Electric", "Acoustic"),
    "feature_2": ("Distorted", "Clear"),
    "feature_3": ("Many Instruments", "Few Instruments"),
    "feature_4": ("Loud", "Soft"),
    "feature_5": ("Heavy", "Light"),
    "feature_6": ("High pitch", "Low pitch"),
    "feature_7": ("Wide pitch variation", "Narrow pitch variation"),
    "feature_8": ("Punchy", "Smooth"),
    "feature_9": ("Harmonious", "Disharmonious"),
    "feature_10": ("Clear melody", "No melody"),
    "feature_11": ("Repetitive", "Non-repetitive"),
    "feature_12": ("Complex rhythm", "Simple rhythm"),
    "feature_13": ("Fast tempo", "Slow tempo"),
    "feature_14": ("Dense", "Sparse"),
    "feature_15": ("Strong beat", "Weak beat"),
}

renamed_music_perceptual_features = {k: "/".join(v) for k, v in music_perceptual_features.items()}

for k_old, k_new in renamed_music_perceptual_features.items():
    music_perceptual_features[k_new] = music_perceptual_features.pop(k_old)

def get_fields(experiment):
    if experiment == "mm":
        return emotion_fields, renamed_emotions
    elif experiment == "mf":
        return music_perceptual_features, renamed_music_perceptual_features
    else:
        raise ValueError("Invalid experiment, must be 'mm' or 'mf'.")

def contingency_tables(
    groundtruth_df,
    field,
    target_grouping=None,
    merge_cases=None):
    if merge_cases is None:
        # merge_cases is supposed to be a list of dictionaries (can't think of a better way...)
        merge_cases = (
            []
        )  # e.g. [ {"merged_name": "<merged_name>", "cases_to_merge": ["foo", "bar"]} ]
    if target_grouping is None:
        target_grouping = {
            "grouping_var": "all_genders",
            "targets": ["Girls/women", "Boys/men", "Mixed"],
        }

    field_counts = groundtruth_df.groupby(field).count()["download"].rename("count")
    global_tot = len(groundtruth_df)

    field_by_target_counts = (
        groundtruth_df.groupby([target_grouping["grouping_var"], field])
        .count()["download"]
        .rename("count")
    )

    contingency_table = pd.DataFrame(columns=["cases"] + target_grouping["targets"])

    for case in groundtruth_df[field].unique():
        row = {"cases": case}
        try:
            global_frac = field_counts.loc[case]
        except KeyError:
            global_frac = 0

        print(f"\n\n{case}: {100 * global_frac / global_tot:.1f}% ({global_frac})")

        for target in target_grouping["targets"]:
            tot = field_by_target_counts.loc[target].sum()
            try:
                frac = field_by_target_counts.loc[target, case]
            except KeyError:
                frac = 0
            row[target] = frac
            print(f"\t{target}: {100 * frac / tot:.1f}% ({frac})", end=" ")

        # overtly complicated, but pandas is deprecating df.append(row) for some stupid reason
        contingency_table = pd.concat(
            [contingency_table, pd.Series(row).to_frame().T], ignore_index=True
        )

    contingency_table.set_index("cases", inplace=True)

    # delete empty rows from contingency table
    for case in groundtruth_df[field].unique():
        if contingency_table.loc[case].sum(axis=0) == 0:
            contingency_table = contingency_table.drop([case])

    # merge cases
    for merging_dict in merge_cases:
        merged_row = pd.Series({k: 0 for k in target_grouping["targets"]})
        for case in merging_dict["cases_to_merge"]:
            merged_row += contingency_table.loc[case]
            contingency_table = contingency_table.drop([case])

        contingency_table.loc[merging_dict["merged_name"]] = merged_row

    chi2, p, dof, expected = chi2_contingency(contingency_table.values)

    print("\n\nChi-square test of independence of variables of the contingency table:")
    print(
        f"\tChi2({dof}, N={contingency_table.sum().sum()})={chi2:.2f}, p={p:.4f}."
        f"\n\t{(expected < 5).sum()} expected freq. cells are below 5 ({100 * (expected < 5).sum() / expected.size:.2f}%)."
    )

    return contingency_table, expected


def anova_by_variable(
    grouping_var,
    ratings_df,
    groundtruth_df,
    experiment,
    categories_to_fuse=None,
    fused_label=None,
    excluded_categories=None,
    groups=None,
    labels=None):
    fields, _ = get_fields(experiment)
    ordered_fields = list(fields.keys())

    if groups is None:
        groups, labels = process_categories(
            categories_to_fuse, fused_label, excluded_categories, 
            groundtruth_df, grouping_var
        )

    # reduce ratings_df to only the rows from the groups
    temp_idx = pd.Index([])
    for index in groups:
        temp_idx = temp_idx.union(index)
    reduced_ratings_df = ratings_df.loc[temp_idx].copy()

    for group, label in zip(groups, labels):
        # add the labels
        reduced_ratings_df.loc[group, grouping_var] = label

    # extract the values by group
    values_by_group = [
        reduced_ratings_df.loc[group][ordered_fields].values 
        for group in groups
    ]

    problematic_vars = perform_statistical_tests(
        values_by_group, labels, ordered_fields
    )

    significant_fields = perform_anova(
        values_by_group, labels, problematic_vars, ordered_fields
    )
    
    

    return significant_fields


def process_categories(
    categories_to_fuse, 
    fused_label, 
    excluded_categories, 
    groundtruth_df, 
    var):

    categories_to_fuse = [] if categories_to_fuse is None else categories_to_fuse
    fused_label = "/".join(categories_to_fuse) if fused_label is None else fused_label
    excluded_categories = [] if excluded_categories is None else excluded_categories

    unique_categories = groundtruth_df[var].unique().tolist()
    df_by_variable = groundtruth_df.reset_index().set_index([var, "stimulus_id"])
    groups = []
    labels = []

    for category in unique_categories:
        if category not in categories_to_fuse + excluded_categories:
            groups.append(df_by_variable.loc[category].index)
            labels.append(category)

    if categories_to_fuse:
        temp_fused = pd.Index([])
        for category in categories_to_fuse:
            if category not in excluded_categories:
                temp_fused = temp_fused.union(df_by_variable.loc[category].index)
        groups.append(temp_fused)
        labels.append(fused_label)

    return groups, labels

def perform_statistical_tests(values_by_group, labels, ordered_fields, print_results=True):
    problematic_variables = []

    if print_results:
        print("\nBartlett's test for equal variances")
    for i, field in enumerate(ordered_fields):
        #print(f"\t{field}, {i}")

        try:
            _, p = bartlett(*[grouped_values[:, i] for grouped_values in values_by_group])
        except RuntimeWarning as w:
            if "divide by zero" in str(w):
                p = -1
            
            if print_results:
                print(f"\t{field}, {w}")


        if p < 0.05:
            warning_message = f"{field} \033[91mp={p:.2E}\033[0m"
            # warnings.warn(
            #     f"The following variable does not have equal variance across groups: "
            #     + warning_message
            # )
            if print_results:
                print(f"\t{warning_message}")
            problematic_variables.append(field)
    
    if print_results and not problematic_variables:
        print("\tAll variables have equal variance across groups.")
    
    # only perform Shapiro-Wilk test for normality if the variances are equal
    ordered_fields = [field for field in ordered_fields if field not in problematic_variables]

    if print_results:
        print("\nShapiro-Wilk test for normality")
    for i, field in enumerate(ordered_fields):
        if print_results:
            print(f"\t{field}")
        for grouped_values, label in zip(values_by_group, labels):

            try:
                _, p = shapiro(grouped_values[:, i])
            except RuntimeWarning as w:
                if "Input data for shapiro has range zero." in str(w):
                    p = -1
                
                if print_results:
                    print(f"\t{field}, {w}")

            if p < 0.05:
                warning_message = f"{label} \033[91mp={p:.2E}\033[0m"
                # warnings.warn(
                #     f"{field} is not normally distributed within the following group: "
                #     + warning_message
                # )
                problematic_variables.append(field)
                if label != labels[-1]:
                    if print_results:
                        print(f"\t\t{warning_message}", end=" ")
                else:
                    if print_results:
                        print(f"\t\t{warning_message}")
            else:
                if label != labels[-1]:
                    if print_results:
                        print(f"\t\t{label} p={p:.2E}", end=" ")
                else:
                    if print_results:
                        print(f"\t\t{label} p={p:.2E}")

    return problematic_variables

def perform_anova(values_by_group, labels, problematic_vars, ordered_fields, alpha=0.05, control_ratings = False):
    significant_fields = []

    # ANOVA
    print("\nOne-way ANOVA (F-test), or Kruskal-Wallis (H-test)")
    F, p = f_oneway(*values_by_group)

    # print number of rows by group
    for i, label in enumerate(labels):
        n = values_by_group[i].shape[0] if not control_ratings else int(values_by_group[i].shape[0]/6)
        print(f"\t{label} N={n:d}")

    for i, field in enumerate(ordered_fields):
        if field in problematic_vars:
            H, p_temp = kruskal(*[values[:, i] for values in values_by_group])
            F_or_H = ("\033[96mH\033[0m", H)
        else:
            F_or_H = ("F", F[i])
            p_temp = p[i]

        if p_temp < alpha:
            significant_fields.append(field)
            result_message = (
                f"\t{field}: {F_or_H[0]}={F_or_H[1]:.2f}, \033[91mp={p_temp:.2E}\033[0m"
            )
            print(result_message)

        if p_temp < alpha:
            for j, label in enumerate(labels):
                print(
                    f"\t\t{label} avg: {values_by_group[j][:,i].mean():.2f}"
                )

    if not significant_fields:
        print("\tNo significant differences.")

    return significant_fields

        