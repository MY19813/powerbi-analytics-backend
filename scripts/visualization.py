import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Circle, Rectangle
import seaborn as sns
import numpy as np
from pathlib import Path
from datetime import datetime
import json

class DataVisualizer:
    """Generate static visualizations for Power BI data"""
    
    def __init__(self, data_file, output_dir):
        """
        Initialize visualizer
        
        Args:
            data_file: Path to processed JSON data
            output_dir: Directory to save charts
        """
        self.data_file = data_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load data
        with open(data_file, 'r') as f:
            self.data = json.load(f)
        self.df = pd.DataFrame(self.data)
        
        # Set style
        self._setup_style()
        
    def _setup_style(self):
        """Set up consistent styling for all charts"""
        # Use seaborn style
        sns.set_style("whitegrid")
        sns.set_palette("husl")
        
        # Set default figure size
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['figure.dpi'] = 100
        
        # Font sizes
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        
        # Colors
        self.colors = {
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#9b59b6'
        }
        
    def generate_all_charts(self):
        """Generate all visualizations"""
        print("\n" + "="*60)
        print("PHASE 2: GENERATING STATIC VISUALIZATIONS")
        print("="*60)
        
        charts_generated = []
        
        # 1. Status Distribution
        print("\n1. Generating Status Distribution (Donut Chart)...")
        self.plot_status_distribution()
        charts_generated.append("status_distribution.png")
        
        # 2. Payment Status
        print("2. Generating Payment Status (Pie Chart)...")
        self.plot_payment_status()
        charts_generated.append("payment_status.png")
        
        # 3. Badge Category Distribution
        print("3. Generating Badge Category Distribution (Bar Chart)...")
        self.plot_badge_categories()
        charts_generated.append("badge_categories.png")
        
        # 4. Revenue Distribution
        print("4. Generating Revenue Distribution (Histogram)...")
        self.plot_revenue_distribution()
        charts_generated.append("revenue_distribution.png")
        
        # 5. Top Countries
        print("5. Generating Top Countries (Horizontal Bar Chart)...")
        self.plot_top_countries()
        charts_generated.append("top_countries.png")
        
        # 6. Top Industries
        print("6. Generating Top Industries (Horizontal Bar Chart)...")
        self.plot_top_industries()
        charts_generated.append("top_industries.png")
        
        # 7. Company Types
        print("7. Generating Company Types (Pie Chart)...")
        self.plot_company_types()
        charts_generated.append("company_types.png")
        
        # 8. Registration Sources
        print("8. Generating Registration Sources (Bar Chart)...")
        self.plot_registration_sources()
        charts_generated.append("registration_sources.png")
        
        # 9. Payment Methods
        print("9. Generating Payment Methods (Bar Chart)...")
        self.plot_payment_methods()
        charts_generated.append("payment_methods.png")
        
        # 10. Key Metrics Dashboard
        print("10. Generating Key Metrics Dashboard...")
        self.plot_key_metrics_dashboard()
        charts_generated.append("key_metrics_dashboard.png")
        
        print("\n" + "="*60)
        print(f"✓ Generated {len(charts_generated)} charts")
        print(f"✓ Saved to: {self.output_dir}")
        print("="*60)
        
        return charts_generated
    
    def plot_status_distribution(self):
        """Donut chart for registration status"""
        if 'status' not in self.df.columns:
            print("  ⚠ 'status' column not found, skipping...")
            return
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get value counts
        status_counts = self.df['status'].value_counts()
        
        # Create donut chart
        colors = ['#2ecc71', '#e74c3c', '#f39c12', '#3498db', '#9b59b6']
        # Ensure that .values is a numpy array and .index is a list of strings
        values = np.array(status_counts.values)
        labels: list[str] = [str(x) for x in status_counts.index]
        pie_result = ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(status_counts)],
            pctdistance=0.85
        )
        
        if len(pie_result) == 3:
            wedges, texts, autotexts = pie_result
        else:
            wedges, texts = pie_result
            autotexts = []
        
        # Draw circle in center for donut effect
        centre_circle = Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        
        # Styling
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')
        
        ax.set_title('Registration Status Distribution', fontsize=16, weight='bold', pad=20)
        
        # Add legend with counts
        legend_labels = [f'{k}: {v}' for k, v in status_counts.items()]
        ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'status_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved status_distribution.png")
    
    def plot_payment_status(self):
        """Pie chart for payment status"""
        if 'payment_status' not in self.df.columns:
            print("  ⚠ 'payment_status' column not found, skipping...")
            return
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        payment_counts = self.df['payment_status'].value_counts()
        
        colors = ['#2ecc71', '#e74c3c', '#3498db']
        pie_values = np.array(payment_counts.values)
        pie_labels: list[str] = [str(x) for x in payment_counts.index]
        pie_result = ax.pie(
            pie_values,
            labels=pie_labels,
            autopct='%1.1f%%',
            startangle=45,
            colors=colors[:len(payment_counts)],
            explode=[0.05] * len(payment_counts)
        )
        
        if len(pie_result) == 3:
            wedges, texts, autotexts = pie_result
        else:
            wedges, texts = pie_result
            autotexts = []
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        ax.set_title('Payment Status Distribution', fontsize=16, weight='bold', pad=20)
        
        legend_labels = [f'{k}: {v}' for k, v in payment_counts.items()]
        ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'payment_status.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved payment_status.png")
    
    def plot_badge_categories(self):
        """Horizontal bar chart for badge categories"""
        if 'badgeCategory_name' not in self.df.columns:
            print("  ⚠ 'badgeCategory_name' column not found, skipping...")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Get counts and sort
        badge_counts = self.df['badgeCategory_name'].value_counts().sort_values()
        
        # Create horizontal bar chart
        bars = ax.barh(range(len(badge_counts)), np.array(badge_counts.values), color=self.colors['primary'])
        ax.set_yticks(range(len(badge_counts)))
        ax.set_yticklabels(badge_counts.index)
        
        # Add value labels on bars
        for i, (idx, value) in enumerate(badge_counts.items()):
            ax.text(value + 2, i, str(value), va='center', fontsize=10, weight='bold')
        
        ax.set_xlabel('Number of Registrations', fontsize=12, weight='bold')
        ax.set_title('Badge Category Distribution', fontsize=16, weight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'badge_categories.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved badge_categories.png")
    
    def plot_revenue_distribution(self):
        """Histogram for revenue distribution"""
        if 'paid_amount_egp' not in self.df.columns:
            print("  ⚠ 'paid_amount_egp' column not found, skipping...")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # EGP Distribution
        paid_egp = self.df[self.df['paid_amount_egp'] > 0]['paid_amount_egp']
        ax1.hist(paid_egp, bins=20, color=self.colors['success'], edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Amount (EGP)', fontsize=12, weight='bold')
        ax1.set_ylabel('Frequency', fontsize=12, weight='bold')
        ax1.set_title('Revenue Distribution (EGP)', fontsize=14, weight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add statistics
        mean_egp = float(paid_egp.mean())
        median_egp = float(np.median(paid_egp))
        ax1.axvline(mean_egp, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_egp:.2f}')
        ax1.axvline(median_egp, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_egp:.2f}')
        ax1.legend()
        
        # USD Distribution
        paid_usd = self.df[self.df['paid_amount_usd'] > 0]['paid_amount_usd']
        ax2.hist(paid_usd, bins=20, color=self.colors['info'], edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Amount (USD)', fontsize=12, weight='bold')
        ax2.set_ylabel('Frequency', fontsize=12, weight='bold')
        ax2.set_title('Revenue Distribution (USD)', fontsize=14, weight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        mean_usd = float(paid_usd.mean())
        median_usd = float(np.median(paid_usd))
        ax2.axvline(mean_usd, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_usd:.2f}')
        ax2.axvline(median_usd, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_usd:.2f}')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'revenue_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved revenue_distribution.png")
    
    def plot_top_countries(self, top_n=15):
        """Horizontal bar chart for top countries"""
        if 'Country_of_Residence' not in self.df.columns:
            print("  ⚠ 'Country_of_Residence' column not found, skipping...")
            return
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Get top countries
        country_counts = self.df['Country_of_Residence'].value_counts().head(top_n).sort_values()
        
        # Create horizontal bar chart
        bars = ax.barh(range(len(country_counts)), np.array(country_counts.values), 
                       color=cm.get_cmap('viridis')(np.linspace(0.3, 0.9, len(country_counts))))
        ax.set_yticks(range(len(country_counts)))
        ax.set_yticklabels(country_counts.index)
        
        # Add value labels
        for i, (idx, value) in enumerate(country_counts.items()):
            ax.text(value + 1, i, str(value), va='center', fontsize=10, weight='bold')
        
        ax.set_xlabel('Number of Registrations', fontsize=12, weight='bold')
        ax.set_title(f'Top {top_n} Countries by Registration', fontsize=16, weight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_countries.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved top_countries.png")
    
    def plot_top_industries(self, top_n=15):
        """Horizontal bar chart for top industries"""
        if 'Industry' not in self.df.columns:
            print("  ⚠ 'Industry' column not found, skipping...")
            return
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Get top industries
        industry_counts = self.df['Industry'].value_counts().head(top_n).sort_values()
        
        bars = ax.barh(range(len(industry_counts)), np.array(industry_counts.values),
                       color=cm.get_cmap('plasma')(np.linspace(0.3, 0.9, len(industry_counts))))
        ax.set_yticks(range(len(industry_counts)))
        ax.set_yticklabels(industry_counts.index, fontsize=9)
        
        for i, (idx, value) in enumerate(industry_counts.items()):
            ax.text(value + 1, i, str(value), va='center', fontsize=10, weight='bold')
        
        ax.set_xlabel('Number of Registrations', fontsize=12, weight='bold')
        ax.set_title(f'Top {top_n} Industries', fontsize=16, weight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'top_industries.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved top_industries.png")
    
    def plot_company_types(self):
        """Pie chart for company types"""
        if 'Company_Type' not in self.df.columns:
            print("  ⚠ 'Company_Type' column not found, skipping...")
            return
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        company_counts = self.df['Company_Type'].value_counts()
        
        colors = sns.color_palette("Set2", len(company_counts))
        company_values = np.array(company_counts.values)
        company_labels: list[str] = [str(x) for x in company_counts.index]
        pie_result = ax.pie(
            company_values,
            labels=company_labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )
        
        if len(pie_result) == 3:
            wedges, texts, autotexts = pie_result
        else:
            wedges, texts = pie_result
            autotexts = []
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        ax.set_title('Company Type Distribution', fontsize=16, weight='bold', pad=20)
        
        legend_labels = [f'{k}: {v}' for k, v in company_counts.items()]
        ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'company_types.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved company_types.png")
    
    def plot_registration_sources(self):
        """Bar chart for registration sources"""
        if 'source' not in self.df.columns:
            print("  ⚠ 'source' column not found, skipping...")
            return
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        source_counts = self.df['source'].value_counts().sort_values(ascending=False)
        
        bars = ax.bar(range(len(source_counts)), np.array(source_counts.values), color=self.colors['primary'])
        ax.set_xticks(range(len(source_counts)))
        ax.set_xticklabels(source_counts.index, rotation=45, ha='right')
        
        # Add value labels on top of bars
        for i, (idx, value) in enumerate(source_counts.items()):
            ax.text(i, value + 5, str(value), ha='center', va='bottom', fontsize=10, weight='bold')
        
        ax.set_ylabel('Number of Registrations', fontsize=12, weight='bold')
        ax.set_title('Registration Sources', fontsize=16, weight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'registration_sources.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved registration_sources.png")
    
    def plot_payment_methods(self):
        """Bar chart for payment methods"""
        if 'payment_card' not in self.df.columns:
            print("  ⚠ 'payment_card' column not found, skipping...")
            return
        
        # Filter only paid records
        paid_df = self.df[self.df['payment_status'] == 'Paid']
        
        if len(paid_df) == 0:
            print("  ⚠ No paid records found, skipping...")
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        payment_counts = pd.Series(paid_df['payment_card']).value_counts()
        
        bars = ax.bar(range(len(payment_counts)), np.array(payment_counts.values), 
                     color=cm.get_cmap('Set3')(np.linspace(0, 1, len(payment_counts))))
        ax.set_xticks(range(len(payment_counts)))
        ax.set_xticklabels(payment_counts.index, rotation=45, ha='right')
        
        for i, (idx, value) in enumerate(payment_counts.items()):
            ax.text(i, value + 1, str(value), ha='center', va='bottom', fontsize=10, weight='bold')
        
        ax.set_ylabel('Number of Transactions', fontsize=12, weight='bold')
        ax.set_title('Payment Methods Used', fontsize=16, weight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'payment_methods.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved payment_methods.png")
    
    def plot_key_metrics_dashboard(self):
        """Create a dashboard with key metrics"""
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle('AI Everything Conference - Registration Analytics Dashboard', 
                    fontsize=20, weight='bold', y=0.98)
        
        # KPI Cards (top row)
        self._add_kpi_card(fig, gs[0, 0], 'Total\nRegistrations', len(self.df), self.colors['primary'])
        
        completed_rate = (self.df['status'] == 'Completed').sum() / len(self.df) * 100 if 'status' in self.df.columns else 0
        self._add_kpi_card(fig, gs[0, 1], 'Completion\nRate', f'{completed_rate:.1f}%', self.colors['success'])
        
        total_revenue = self.df['paid_amount_egp'].sum() if 'paid_amount_egp' in self.df.columns else 0
        self._add_kpi_card(fig, gs[0, 2], 'Total Revenue\n(EGP)', f'{total_revenue:,.0f}', self.colors['warning'])
        
        # Status breakdown (middle left)
        if 'status' in self.df.columns:
            ax1 = fig.add_subplot(gs[1, 0])
            status_counts = self.df['status'].value_counts()
            ax1.bar(range(len(status_counts)), np.array(status_counts.values), color=sns.color_palette("husl", len(status_counts)))
            ax1.set_xticks(range(len(status_counts)))
            ax1.set_xticklabels(status_counts.index, rotation=45, ha='right', fontsize=9)
            ax1.set_title('Status Breakdown', fontsize=12, weight='bold')
            ax1.grid(axis='y', alpha=0.3)
        
        # Payment status (middle center)
        if 'payment_status' in self.df.columns:
            ax2 = fig.add_subplot(gs[1, 1])
            payment_counts = self.df['payment_status'].value_counts()
            ax2.pie(np.array(payment_counts.values), labels=list(payment_counts.index), autopct='%1.1f%%', 
                   colors=['#2ecc71', '#e74c3c', '#3498db'])
            ax2.set_title('Payment Status', fontsize=12, weight='bold')
        
        # Badge categories (middle right)
        if 'badgeCategory_name' in self.df.columns:
            ax3 = fig.add_subplot(gs[1, 2])
            badge_counts = self.df['badgeCategory_name'].value_counts().head(5)
            ax3.barh(range(len(badge_counts)), np.array(badge_counts.values), color=self.colors['info'])
            ax3.set_yticks(range(len(badge_counts)))
            ax3.set_yticklabels(badge_counts.index, fontsize=9)
            ax3.set_title('Top Badge Categories', fontsize=12, weight='bold')
            ax3.grid(axis='x', alpha=0.3)
        
        # Top countries (bottom left & center)
        if 'Country_of_Residence' in self.df.columns:
            ax4 = fig.add_subplot(gs[2, :2])
            country_counts = self.df['Country_of_Residence'].value_counts().head(10)
            ax4.barh(range(len(country_counts)), np.array(country_counts.values), 
                    color=plt.cm.get_cmap('viridis')(np.linspace(0.3, 0.9, len(country_counts))))
            ax4.set_yticks(range(len(country_counts)))
            ax4.set_yticklabels(country_counts.index, fontsize=9)
            ax4.set_title('Top 10 Countries', fontsize=12, weight='bold')
            ax4.grid(axis='x', alpha=0.3)
        
        # Revenue by badge (bottom right)
        if 'badgeCategory_name' in self.df.columns and 'paid_amount_egp' in self.df.columns:
            ax5 = fig.add_subplot(gs[2, 2])
            revenue_by_badge = pd.Series(self.df.groupby('badgeCategory_name')['paid_amount_egp'].sum()).sort_values(ascending=False).head(5)
            ax5.bar(range(len(revenue_by_badge)), np.array(revenue_by_badge.values), color=self.colors['warning'])
            ax5.set_xticks(range(len(revenue_by_badge)))
            ax5.set_xticklabels(revenue_by_badge.index, rotation=45, ha='right', fontsize=8)
            ax5.set_title('Revenue by Badge', fontsize=12, weight='bold')
            ax5.set_ylabel('Revenue (EGP)', fontsize=10)
            ax5.grid(axis='y', alpha=0.3)
        
        plt.savefig(self.output_dir / 'key_metrics_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Saved key_metrics_dashboard.png")
    
    def _add_kpi_card(self, fig, grid_spec, title, value, color):
        """Helper to add KPI card to dashboard"""
        ax = fig.add_subplot(grid_spec)
        ax.axis('off')
        
        # Background
        ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=color, alpha=0.2))
        
        # Text
        ax.text(0.5, 0.65, str(value), ha='center', va='center', 
               fontsize=32, weight='bold', color=color)
        ax.text(0.5, 0.35, title, ha='center', va='center', 
               fontsize=14, weight='bold', color='#2c3e50')