from selenium import webdriver
from selenium.webdriver.common.by import By
import argparse

'''Following functions required installing geckodriver.
You can do it from this repo: https://github.com/mozilla/geckodriver/releases'''


# cutting fasta file to files with max 10 sequences (required by xtalpred)
def splitting_fasta(file_name):
    with open(file_name) as file:
        lines = file.readlines()
        i = 0
        pom = 0
        for line in lines:
            with open(f"{i}_{file_name}", "a") as fasta_file:
                if line[0] == ">":
                    pom += 1
                    if pom == 10:
                        i += 1
                        pom = 0
                        with open(f"{i}_{file_name}", "a") as fasta_file:
                            fasta_file.write(line)
                    else:
                        id = line[:line.find("_")]
                        fasta_file.write(f"{id}\n")
                else:
                    fasta_file.write(line)
    return i


# the function automatically submits data on xtalpred. The results will be send on given mail, when the job is finished
def submit_to_xtalpred(e_mail, fasta_file):
    number_of_files = splitting_fasta(fasta_file)
    driver = webdriver.Firefox(executable_path='geckodriver')
    for i in range(0, number_of_files + 1):
        driver.get("https://xtalpred.godziklab.org/XtalPred-cgi/xtal.pl")
        driver.find_element(By.NAME, "mail").send_keys(e_mail)
        with open(f"{i}_{fasta_file}") as file:
            file = file.read()
            driver.find_element(By.NAME, "query").send_keys(file)
        driver.find_element(By.NAME, "CMG").click()
        driver.find_element(By.NAME, "agree").click()
        driver.find_element(By.NAME, "Submit").click()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Enter the address to which you want to receive the results and the path to the fasta file")
    parser.add_argument('mail', type=str, help="your email")
    parser.add_argument('path', type=str, help="path to fasta file")
    args = parser.parse_args()
    submit_to_xtalpred(args.mail, args.path)
