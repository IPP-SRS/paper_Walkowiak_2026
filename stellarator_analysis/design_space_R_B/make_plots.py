import matplotlib.pyplot as plt
from process.io.mfile import MFile
import numpy as np
import os
from dataclasses import dataclass, field


class Settings:
    """
    Settings for the plotting module.
    """
    main_name = 'results'
    prefix = 'squid'
    var_name = 'b_plasma_toroidal_on_axis'
    var_label = 'B (T)'
    workdir = os.path.dirname(os.path.realpath(__file__))
    exclusion_list = ['HTS_high_stress']
    

def main(main_name=Settings.main_name):
    """
    Collect and plot output from MFILE.DAT in main_name directory
    prefix is a name of the MFILE.DAT file
    param is PROCESS parameter name loaded form the input
    """
    case_dir = Settings.workdir
    caselist = [case for case in os.listdir(case_dir) 
                if (os.path.isdir(os.path.join(case_dir, case))
                    and case not in Settings.exclusion_list)]
    print(caselist)

    for case in caselist:
        print(f'Processing case: {case}')
        subdir = os.path.join(Settings.workdir, case, main_name)

        # plot_coe_capcost(subdir)
        # plot_parameters(subdir)
        plot_parameters2(subdir)
        plot_parameters3(subdir)
        # # plot_constrains(subdir)
        plot_constrains(subdir, selected_constrains=['024', '008', '083', '062', '032'])
        plot_R_major(subdir)
        # plot_power(subdir)


def load_results(workdir, var_name, results_name, verbose=False):
    """
    Load results from MFILE.DAT files in the specified directory.
    """
    case_name = []
    results = []
    output = {}

    for case in os.listdir(workdir):   
        mfile_path = os.path.join(workdir, case, Settings.prefix+'.MFILE.DAT')
        if os.path.isfile(mfile_path):
            m = MFile(filename=mfile_path)
            if m.data[results_name].get_number_of_scans() == 1 and m.data['ifail'].get_scan(-1) == 1:
                case_name.append(m.data[var_name].get_scan(-1))
                results.append(m.data[results_name].get_scan(-1))
                output[m.data[var_name].get_scan(-1)] = m.data[results_name].get_scan(-1)

    output = dict(sorted(output.items()))
    if verbose:
        print(f'{results_name} found for {var_name}:')
        for key, value in output.items():
            print(f'{key}: {value}')

    return output


def plot_coe_capcost(workdir, var_name=Settings.var_name):
    """
    Plot COE and capital cost against the variable name on the same plot with two y-axes.
    """

    coe = load_results(workdir, var_name, 'coe', verbose=True)
    capcost = load_results(workdir, var_name, 'capcost', verbose=True)


    fig1, ax1 = plt.subplots(figsize=(7, 5))

    x = list(coe.keys())
    y1 = list(coe.values())
    y2 = list(capcost.values())

    color1 = 'tab:blue'
    ax1.set_xlabel(Settings.var_label)
    ax1.set_ylabel('COE ($/MWh)', color=color1)
    ax1.plot(x, y1, marker='o', linestyle='-', color=color1, label='COE')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(bottom=0, top=max(y1)*1.1)  # Set y-axis from 0 to 110% of max

    ax1.grid(True, which='both', axis='both')  # Turn on grid for x and left y axis

    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Capital Cost (M$)', color=color2)
    ax2.plot(x, y2, marker='o', linestyle='-', color=color2, label='Capital Cost')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(bottom=0, top=max(y2)*1.1)  # Set y-axis from 0 to 110% of max

    plt.title('Cost of Electricity and Capital Cost vs Power')
    fig1.tight_layout()
    # plt.show()
    plt.savefig(os.path.join(os.path.dirname(workdir), 'coe_capcost_plot.png'))


def plot_parameters(workdir, var_name=Settings.var_name):
    """
    Plot parameters: Bt, Rmajor, and aspect ratio against power.
    """

    bt = load_results(workdir, var_name, 'b_plasma_toroidal_on_axis')
    rmajor = load_results(workdir, var_name, 'rmajor')
    aspect = load_results(workdir, var_name, 'coil_aspect')

    fig2, ax1 = plt.subplots(figsize=(7, 5))
    x = list(bt.keys())
    y1 = list(bt.values())
    y2 = list(rmajor.values())
    y3 = list(aspect.values())

    color1 = 'tab:blue'
    ax1.set_xlabel(Settings.var_label)
    ax1.set_ylabel('Bt (T)', color=color1)
    ax1.plot(x, y1, marker='o', linestyle='-', color=color1, label='Bt')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(bottom=min(y1)*0.9, top=max(y1)*1.1)

    ax2 = ax1.twinx()
    color2 = 'tab:green'
    ax2.set_ylabel('Rmajor (m)', color=color2)
    ax2.plot(x, y2, marker='o', linestyle='-', color=color2, label='Rmajor')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(bottom=min(y2)*0.9, top=max(y2)*1.1)

    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Offset the third y-axis
    color3 = 'tab:orange'
    ax3.set_ylabel('Coil Scaling Factor', color=color3)
    ax3.plot(x, y3, marker='o', linestyle='-', color=color3, label='Coil Scaling Factor')
    ax3.tick_params(axis='y', labelcolor=color3)
    ax3.set_ylim(bottom=min(y3)*0.9, top=max(y3)*1.1)

    # plt.title('Bt, Rmajor and Coil scaling vs Power')
    fig2.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(workdir), 'parameters_plot.png'))


def plot_parameters2(workdir, var_name=Settings.var_name):
    """
    Plot parameters: Temperature, Electron Density, and Hfact against power.
    """

    te = load_results(workdir, var_name, 'temp_plasma_electron_vol_avg_kev')
    dene = load_results(workdir, var_name, 'nd_plasma_electrons_vol_avg')
    hfact = load_results(workdir, var_name, 'hfact')

    fig2, ax1 = plt.subplots(figsize=(7, 5))
    x = list(te.keys())
    y1 = list(te.values())
    y2 = list(dene.values())
    y3 = list(hfact.values())

    set_boxes(ax1, labels=False)
    ax1.text(5.8, 8.8, 'Low field', rotation='vertical', va='top', fontsize=10, fontweight='bold')
    ax1.text(6.35, 8.8, 'Optimal field', rotation='vertical', va='top', fontsize=10, fontweight='bold')
    ax1.text(6.9, 8.8, 'High field', rotation='vertical', va='top', fontsize=10, fontweight='bold')

    color1 = 'tab:blue'
    ax1.set_xlabel(Settings.var_label)
    ax1.set_ylabel('Electron temperature (keV)', color=color1)
    ax1.plot(x, y1, marker='o', linestyle='-', color=color1, label='Te')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(bottom=min(y1)*0.9, top=max(y1)*1.1)

    ax2 = ax1.twinx()
    color2 = 'tab:green'
    ax2.set_ylabel('Electron denisty [1/m3]', color=color2)
    ax2.plot(x, y2, marker='o', linestyle='-', color=color2, label='ne')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(bottom=min(y2)*0.9, top=max(y2)*1.1)

    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Offset the third y-axis
    color3 = 'tab:orange'
    ax3.set_ylabel('H-factor', color=color3)
    ax3.plot(x, y3, marker='o', linestyle='-', color=color3, label='h-fact')
    ax3.tick_params(axis='y', labelcolor=color3)
    ax3.set_ylim(bottom=min(y3)*0.9, top=max(y3)*1.1)

    # plt.title('Te, ne and H-fact vs Power')
    fig2.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(workdir), 'parameters2_plot.png'))
    

def plot_parameters3(workdir, var_name=Settings.var_name):
    """
    Plot parameters: Temperature, Electron Density, and Hfact against power.
    """

    te = load_results(workdir, var_name, 'temp_plasma_electron_vol_avg_kev')
    dene = load_results(workdir, var_name, 'nd_plasma_electrons_vol_avg')
    hfact = load_results(workdir, var_name, 'hfact')
    rmajor = load_results(workdir, var_name, 'rmajor')

    fig2, ax0 = plt.subplots(figsize=(7, 5))
    x = list(te.keys())
    y0 = list(rmajor.values())
    y1 = list(te.values())
    y2 = list(dene.values())
    y3 = list(hfact.values())

    set_boxes(ax0, labels=True)

    ax0.set_xlabel(Settings.var_label)
    color2 = 'k'
    ax0.set_ylabel('Rmajor (m)', color=color2, fontweight='bold')
    ax0.plot(x, y0, marker='o', linestyle='-', color=color2, label='Rmajor', markersize=7, linewidth=2.5)
    ax0.tick_params(axis='y', labelcolor=color2)
    ax0.set_ylim(bottom=min(y0)*0.97, top=max(y0)*1.03)    

    ax1 = ax0.twinx()
    ax1.spines['left'].set_position(('outward', 60))  # Offset the axis
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.set_ticks_position('left')
    color1 = 'tab:blue'
    ax1.set_ylabel('Electron temperature (keV)', color=color1)
    ax1.plot(x, y1, marker='o', linestyle='--', color=color1, label='Te', markersize=3)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(bottom=min(y1)*0.8, top=max(y1)*1.2)

    ax2 = ax0.twinx()
    color2 = 'tab:green'
    ax2.set_ylabel('Electron denisty [1/m3]', color=color2)
    ax2.plot(x, y2, marker='o', linestyle='--', color=color2, label='ne', markersize=3)
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(bottom=min(y2)*0.8, top=max(y2)*1.2)

    ax3 = ax0.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Offset the third y-axis
    color3 = 'tab:orange'
    ax3.set_ylabel('H-factor', color=color3)
    ax3.plot(x, y3, marker='o', linestyle='--', color=color3, label='h-fact', markersize=3)
    ax3.tick_params(axis='y', labelcolor=color3)
    ax3.set_ylim(bottom=min(y3)*0.8, top=max(y3)*1.2)

    # plt.title('Te, ne and H-fact vs Power')
    fig2.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(workdir), 'parameters3_plot.png'))

@dataclass
class Constrain:
    """
    Class to hold information about a constraint.
    """
    number: str
    name: str
    results: dict = field(default_factory= lambda: { })

def load_constrains_data(workdir, var_name, selected_constrains=None):
    constrains_id = ['024', '008', '017', '018', '067', '082', '083', '062', '032', '034', '035', '065']
    constrains_names = [
        'Beta', 'Neutron_wall_load', 'Radiation_fraction', 'Divertor_heat_load', 'Radiation Wall load', 'toroidalgap', 'radialspace',
        'f_alpha_confinement', 'TF_coil_stress', 'Dump voltage', 'J_WP / J_p', 'VV stress'
    ]
    list_of_constrains = []

    for idx, name in zip(constrains_id, constrains_names):
        if selected_constrains is None or idx in selected_constrains:
            list_of_constrains.append(Constrain(
                number=idx,
                name=name,
                results=load_results(workdir, var_name, 'ineq_con' + idx)
            ))
        
    return list_of_constrains


def plot_constrains(workdir, var_name=Settings.var_name, selected_constrains=None):
    """
    Plot constrains normalized residues against power.
    """

    list_of_constrains = load_constrains_data(workdir, var_name, selected_constrains)

    fig, ax1 = plt.subplots(figsize=(10, 7))  # Increased figsize for legend

    set_boxes(ax1, labels=False)
    ax1.text(5.8, 0.9, 'Low field', rotation='vertical', va='top', fontsize=10, fontweight='bold')
    ax1.text(6.35, 0.9, 'Optimal field', rotation='vertical', va='top', fontsize=10, fontweight='bold')
    ax1.text(6.9, 0.9, 'High field', rotation='vertical', va='top', fontsize=10, fontweight='bold')

    ax1.set_xlabel(Settings.var_label)
    ax1.set_ylabel('normalised residue')
    ax1.set_ylim(bottom=0, top=1)

    # Use a colormap to assign a unique color to each line
    cmap = plt.get_cmap('tab20')
    num_lines = len(list_of_constrains)
    colors = [cmap(i % 20) for i in range(num_lines)]

    for i, constrain in enumerate(list_of_constrains):
        if selected_constrains is None or constrain.number in selected_constrains:
            ax1.plot(
                constrain.results.keys(),
                constrain.results.values(),
                marker='o',
                linestyle='-',
                label=constrain.name,
                color=colors[i]
            )

    plt.title('Constrains')
    # ax1.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), borderaxespad=0)
    ax1.legend(loc='upper right')
    fig.tight_layout(rect=[0, 0, 0.82, 1])  # Leave space for legend
    plt.savefig(os.path.join(os.path.dirname(workdir), 'constrains_plot.png'))



def plot_power(workdir, var_name=Settings.var_name):

    P_net = load_results(workdir, var_name, 'p_plant_electric_net_mw')
    P_gross = load_results(workdir, var_name, 'p_plant_electric_gross_mw') 
    P_rec = load_results(workdir, var_name, 'p_plant_electric_recirc_mw')
    P_fus = load_results(workdir, var_name, 'p_fusion_total_mw')

    fig, ax1 = plt.subplots(figsize=(7, 5))  # Increased figsize for legend

    ax1.set_xlabel(Settings.var_label)
    ax1.set_ylabel('Power (MW)')
    ax1.set_ylim(bottom=0, top=max(P_fus.values())*1.05)

    ax1.plot(P_net.keys(), P_net.values(), marker='o', linestyle='-', label='P_net')
    ax1.plot(P_net.keys(), P_gross.values(), marker='o', linestyle='-', label='P_gross')
    ax1.plot(P_net.keys(), P_rec.values(), marker='o', linestyle='-', label='P_rec')
    ax1.plot(P_net.keys(), P_fus.values(), marker='o', linestyle='-', label='P_fus')

    plt.title('Power')
    ax1.legend()
    fig.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(workdir), 'power_plot.png'))

def plot_R_major(workdir, var_name=Settings.var_name):
    """
    Plot parameters: Bt, Rmajor, and aspect ratio against power.
    """

    bt = load_results(workdir, var_name, 'b_plasma_toroidal_on_axis')
    rmajor = load_results(workdir, var_name, 'rmajor')

    fig2, ax1 = plt.subplots(figsize=(7, 5))
    x = list(bt.keys())
    y2 = list(rmajor.values())

    ax1.set_xlabel(Settings.var_label)
    color2 = 'k'
    ax1.set_ylabel('Rmajor (m)', color=color2)
    ax1.plot(x, y2, marker='o', linestyle='-', color=color2, label='Rmajor')
    ax1.tick_params(axis='y', labelcolor=color2)
    ax1.set_ylim(bottom=min(y2)*0.95, top=max(y2)*1.05)
    
    set_boxes(ax1)

    fig2.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(workdir), 'R_major_plot.png'))

def set_boxes(ax1, labels=True):
    ax1.set_xlim(5, 9.25)

    # Add boxes
    ymin, ymax = ax1.get_ylim()
    ax1.axvspan(ax1.get_xlim()[0], 6.25, alpha=0.2, color='red')
    ax1.axvspan(6.25, 6.5, alpha=0.2, color='green')
    ax1.axvspan(6.5, ax1.get_xlim()[1], alpha=0.2, color='orange')
    
    if labels:
        # Add text labels to each box
        ax1.text(5.8, 21.3, 'Low field', rotation='vertical', va='top', fontsize=10, fontweight='bold')
        ax1.text(6.35, 21.3, 'Optimal field', rotation='vertical', va='top', fontsize=10, fontweight='bold')
        ax1.text(6.9, 21.3, 'High field', rotation='vertical', va='top', fontsize=10, fontweight='bold')

if __name__ == "__main__":

    main()