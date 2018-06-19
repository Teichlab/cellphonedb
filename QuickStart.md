0. Requisites:
- Python3
- Pip3
- python3-venv


1. Download and unpack CellPhoneDb manager (you need the basic_auth server password)
'''shell
curl 172.27.17.241:8000/downloads/CellPhoneDB-0.0.1.tar.gz -u teichlab --output CellPhoneDB-0.0.1.tar.gz
tar -xzf CellPhoneDB-0.0.1.tar.gz
cd CellPhoneDB-0.0.1
'''

2. Create Virual Env (optional)
'''shell
python3 -m venv cpdb-env
source cpdb-env/bin/activate
python setup.py install
'''

3. Execute example method
FLASK_APP=manage.py flask call_query cluster_statistical_analysis example_data/test_meta.txt example_data/test_counts.txt

4. Running your inputs

Input files (meta and counts) shoud be allocated in 'in' folder and they shoud be in .txt/.tsv for tab separated format or .csv for comma separated format.

Results will be saved in 'out' folder in csv format.


~ Optional parameters (are cumulative):
- iterations (1000): number of iterations for statistical script
- data_path (empty): if you need change the origin of the data path
- output_path (empty): if you need change the path of the results
- means_result_filename (means.txt): result filename for means data
- pvalues_result_filename (pvalues.txt): result filename for pvalues data
- significant_mean_result_filename (significant_means.txt): result filename for significant means data
- means_pvalues_result_filename ('pvalues_means.txt'): result filename for pvalues_means data
- deconvoluted_result_filename ('deconvoluted.txt'): result filename for deconvoluted
- debug_seed (0): set the seed of rand generate data (for debug proposals)