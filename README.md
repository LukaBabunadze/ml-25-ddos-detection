# DDoS Attack Detection from Server Log / DDoS შეტევის გამოვლენა სერვერის ლოგიდან

This project analyzes a server log file to detect potential DDoS attack times using Python. The script processes the log, identifies request spikes, and visualizes the results. / ეს პროექტი აანალიზებს სერვერის ლოგ ფაილს DDoS შეტევის დროის გამოსავლენად Python-ის გამოყენებით. სკრიპტი ამუშავებს ლოგს, გამოავლენს მოთხოვნების მკვეთრ ზრდას და ვიზუალიზაციას ახდენს შედეგების.

## Log File / ლოგ ფაილი
- **Link to Log File / ლოგ ფაილის ბმული**: [luka_babunadze_1_server.log](https://github.com/yourusername/yourrepository/blob/main/luka_babunadze_1_server.log)
- **DDoS Attack Time / DDoS შეტევის დრო**: Max requests: 2268 at 2024-03-22 18:08:30+04:00

## Visualization / ვიზუალიზაცია
### Request Frequency Plot / მოთხოვნების სიხშირის გრაფიკი
![DDoS Detection Plot](ddos_detection_plot.png)

This plot shows requests per 10-second intervals, rolling mean, threshold, and detected DDoS attack times. / ეს გრაფიკი აჩვენებს მოთხოვნებს 10-წამიანი ინტერვალებით, მოძრავ საშუალოს, ზღვარს და გამოვლენილ DDoS შეტევის დროებს.

## How to Run the Code / კოდის გაშვების ინსტრუქცია
### English
1. Clone the repository: `git clone https://github.com/yourusername/yourrepository.git`
2. Install dependencies: `pip install pandas matplotlib scikit-learn`
3. Save the log file as `luka_babunadze_1_server.log` in the repository folder.
4. Run the script: `python ddos_detection.py`
5. Check the output for detected DDoS times and view the generated plots (`ddos_detection_plot.png` and `regression_analysis_plot.png`).

### ქართული
1. გადმოწერეთ რეპოზიტორია: `git clone https://github.com/yourusername/yourrepository.git`
2. დააინსტალირეთ დამოკიდებულებები: `pip install pandas matplotlib scikit-learn`
3. შეინახეთ ლოგ ფაილი სახელით `luka_babunadze_1_server.log` რეპოზიტორიის საქაღალდეში.
4. გაუშვით სკრიპტი: `python ddos_detection.py`
5. შეამოწმეთ გამომავალი DDoS დროებისთვის და ნახეთ გენერირებული გრაფიკები (`ddos_detection_plot.png` და `regression_analysis_plot.png`).

## Key Code Fragments and Explanations / ძირითადი კოდის ფრაგმენტები და ახსნა
### 1. Timestamp Parsing / დროის ანალიზი
```python
def parse_log_line(line):
    pattern = r'$$ (.*?) $$'
    match = re.search(pattern, line)
    if match:
        timestamp_str = match.group(1)
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S%z')
        return timestamp
