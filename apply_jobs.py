from playwright.sync_api import sync_playwright
import pandas as pd
import os

EXCEL_FILE = "naukri_jobs.xlsx"
PROFILE_DIR = "naukri_profile"


def main():

    # Check Excel file
    if not os.path.exists(EXCEL_FILE):
        print("naukri_jobs.xlsx not found.")
        return

    # Check saved Naukri profile
    if not os.path.exists(PROFILE_DIR):
        print("Naukri profile not found.")
        print("Run save_session.py first.")
        return

    # Read Excel
    df = pd.read_excel(EXCEL_FILE)

    if "Job URL" not in df.columns:
        print("Job URL column not found in Excel.")
        return

    with sync_playwright() as p:

        # Open saved Naukri browser profile
        context = p.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=False
        )

        page = context.pages[0] if context.pages else context.new_page()

        print("Naukri browser profile loaded.")
        print("Starting job application process...")

        for index, row in df.iterrows():

            job_url = str(row["Job URL"]).strip()

            if not job_url or job_url == "nan":
                continue

            print()
            print("=" * 70)
            print(f"Job {index + 1} of {len(df)}")
            print(job_url)

            try:

                # Open job
                page.goto(
                    job_url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                page.wait_for_timeout(5000)

                print("Job page opened.")

                # Scroll through page
                page.mouse.wheel(0, 1200)
                page.wait_for_timeout(2000)

                # Find Apply button
                apply_button = page.get_by_text(
                    "Apply",
                    exact=True
                ).first

                if apply_button.is_visible():

                    print("Apply button found.")

                    # Click Apply
                    apply_button.click()

                    page.wait_for_timeout(4000)

                    print("Apply button clicked.")

                    print()
                    print("IMPORTANT:")
                    print("If Naukri asks for:")
                    print("- Resume upload")
                    print("- Profile information")
                    print("- Questions")
                    print("- CAPTCHA")
                    print("- Final Submit")
                    print()
                    print("Complete/review it manually.")
                    print("Automation will NOT submit the final application.")

                    input(
                        "After you finish reviewing this job, "
                        "press ENTER to continue..."
                    )

                else:

                    print("Apply button not found.")
                    print("Skipping this job.")

            except Exception as e:

                print("Error:", e)
                print("Skipping this job.")

        print()
        print("=" * 70)
        print("All jobs processed.")

        input("Press ENTER to close the browser...")

        context.close()


if __name__ == "__main__":
    main()