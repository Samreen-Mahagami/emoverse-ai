"""
EmoVerse AI - Architecture Diagram Generator
Creates a visual architecture diagram for AWS AI Agent Global Hackathon
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Color scheme
    colors = {
        'frontend': '#E3F2FD',
        'api': '#FFF3E0', 
        'ai': '#E8F5E8',
        'storage': '#E1F5FE',
        'agent': '#F3E5F5',
        'security': '#FFEBEE',
        'external': '#F5F5F5'
    }
    
    # Title
    ax.text(8, 11.5, 'EmoVerse AI - Social Emotional Learning Platform', 
            fontsize=20, fontweight='bold', ha='center')
    ax.text(8, 11, 'AWS AI Agent Global Hackathon Architecture', 
            fontsize=14, ha='center', style='italic')
    
    # Frontend Layer
    frontend_box = FancyBboxPatch((0.5, 9), 3, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['frontend'],
                                  edgecolor='#1976D2', linewidth=2)
    ax.add_patch(frontend_box)
    ax.text(2, 9.75, '👨‍🎓👩‍🏫 Users', fontsize=12, fontweight='bold', ha='center')
    ax.text(2, 9.4, 'Streamlit App', fontsize=10, ha='center')
    ax.text(2, 9.1, 'Multi-user Interface', fontsize=9, ha='center')
    
    # API Gateway & Lambda
    api_box = FancyBboxPatch((5, 9), 3, 1.5,
                             boxstyle="round,pad=0.1",
                             facecolor=colors['api'],
                             edgecolor='#F57C00', linewidth=2)
    ax.add_patch(api_box)
    ax.text(6.5, 9.75, '🚪 API Gateway', fontsize=12, fontweight='bold', ha='center')
    ax.text(6.5, 9.4, '⚡ AWS Lambda', fontsize=10, ha='center')
    ax.text(6.5, 9.1, 'Orchestration', fontsize=9, ha='center')
    
    # AI Services
    ai_box = FancyBboxPatch((9, 8.5), 6, 2.5,
                            boxstyle="round,pad=0.1",
                            facecolor=colors['ai'],
                            edgecolor='#388E3C', linewidth=2)
    ax.add_patch(ai_box)
    ax.text(12, 10.7, '🧠 AI/ML Services', fontsize=12, fontweight='bold', ha='center')
    
    # Individual AI services
    ax.text(10.5, 10.3, '🧠 Bedrock\n(Claude Sonnet)', fontsize=9, ha='center')
    ax.text(13.5, 10.3, '💭 Comprehend\n(Sentiment)', fontsize=9, ha='center')
    ax.text(10.5, 9.7, '📄 Textract\n(OCR)', fontsize=9, ha='center')
    ax.text(13.5, 9.7, '🎤 Transcribe\n(Voice)', fontsize=9, ha='center')
    ax.text(12, 9.1, 'Grade-Appropriate Content Generation', fontsize=9, ha='center', style='italic')
    
    # Storage Services
    storage_box = FancyBboxPatch((0.5, 6.5), 4, 2,
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['storage'],
                                 edgecolor='#0277BD', linewidth=2)
    ax.add_patch(storage_box)
    ax.text(2.5, 8.2, '📦 Storage & Data', fontsize=12, fontweight='bold', ha='center')
    ax.text(1.5, 7.7, '📦 S3\nDocuments', fontsize=9, ha='center')
    ax.text(3.5, 7.7, '🗄️ DynamoDB\nAnalytics', fontsize=9, ha='center')
    ax.text(2.5, 6.9, 'Student Progress & Memory', fontsize=9, ha='center', style='italic')
    
    # AI Agent Runtime
    agent_box = FancyBboxPatch((5.5, 6), 5, 3,
                               boxstyle="round,pad=0.1",
                               facecolor=colors['agent'],
                               edgecolor='#7B1FA2', linewidth=2)
    ax.add_patch(agent_box)
    ax.text(8, 8.7, '🤖 AI Agent Runtime', fontsize=12, fontweight='bold', ha='center')
    
    # Agent components
    ax.text(6.5, 8.2, 'Tier 1: Direct\nGeneration', fontsize=9, ha='center')
    ax.text(8, 8.2, 'Tier 2: Smart\nRegeneration', fontsize=9, ha='center')
    ax.text(9.5, 8.2, 'Tier 3: External\nDiscovery', fontsize=9, ha='center')
    
    ax.text(6.5, 7.5, '🧠 Memory', fontsize=9, ha='center')
    ax.text(8, 7.5, '👁️ Observability', fontsize=9, ha='center')
    ax.text(9.5, 7.5, '🌐 Playwright', fontsize=9, ha='center')
    
    ax.text(8, 6.4, 'Multi-Tier Intelligent Content System', fontsize=9, ha='center', style='italic')
    
    # Security
    security_box = FancyBboxPatch((11.5, 6.5), 3.5, 2,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['security'],
                                  edgecolor='#C62828', linewidth=2)
    ax.add_patch(security_box)
    ax.text(13.25, 8.2, '🔐 Security', fontsize=12, fontweight='bold', ha='center')
    ax.text(12.5, 7.7, '🔐 Cognito\nAuth', fontsize=9, ha='center')
    ax.text(14, 7.7, '🛡️ IAM\nAccess', fontsize=9, ha='center')
    ax.text(13.25, 6.9, 'User Management', fontsize=9, ha='center', style='italic')
    
    # External Resources
    external_box = FancyBboxPatch((1, 3.5), 14, 1.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['external'],
                                  edgecolor='#424242', linewidth=2)
    ax.add_patch(external_box)
    ax.text(8, 4.7, '🌐 External Educational Resources', fontsize=12, fontweight='bold', ha='center')
    ax.text(4, 4.2, '📚 Storyline Online', fontsize=10, ha='center')
    ax.text(8, 4.2, '🎨 Storyberries', fontsize=10, ha='center')
    ax.text(12, 4.2, '🧠 KidsKonnect SEL', fontsize=10, ha='center')
    ax.text(8, 3.8, 'AI Agent discovers additional content when needed', fontsize=9, ha='center', style='italic')
    
    # Data Flow Arrows
    # Frontend to API
    arrow1 = ConnectionPatch((3.5, 9.75), (5, 9.75), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, 
                            mutation_scale=20, fc="black", lw=2)
    ax.add_patch(arrow1)
    
    # API to AI Services
    arrow2 = ConnectionPatch((8, 9.75), (9, 9.75), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5,
                            mutation_scale=20, fc="black", lw=2)
    ax.add_patch(arrow2)
    
    # API to Storage
    arrow3 = ConnectionPatch((6, 9), (3, 8.5), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5,
                            mutation_scale=20, fc="blue", lw=2)
    ax.add_patch(arrow3)
    
    # API to Agent
    arrow4 = ConnectionPatch((6.5, 9), (7.5, 8.5), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5,
                            mutation_scale=20, fc="purple", lw=2)
    ax.add_patch(arrow4)
    
    # Agent to External
    arrow5 = ConnectionPatch((8, 6), (8, 5), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5,
                            mutation_scale=20, fc="gray", lw=2)
    ax.add_patch(arrow5)
    
    # Key Features Box
    features_box = FancyBboxPatch((1, 0.5), 14, 2.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor='#FFFDE7',
                                  edgecolor='#F57F17', linewidth=2)
    ax.add_patch(features_box)
    ax.text(8, 2.7, '⭐ Key Platform Features', fontsize=14, fontweight='bold', ha='center')
    
    features_text = """
    📚 Multi-Modal Input: PDF, Images, Voice Questions  |  🎯 Grade-Adaptive Content (K-10)  |  🤖 3-Tier AI Agent System
    📊 Real-Time Analytics Dashboard  |  💭 Sentiment-Aware Learning  |  🌐 External Content Discovery
    👥 Multi-User Support with Session Isolation  |  ⚡ Serverless Scalable Architecture  |  🔒 Secure Authentication
    """
    
    ax.text(8, 1.5, features_text, fontsize=10, ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig('emoverse_ai_architecture.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.savefig('emoverse_ai_architecture.pdf', bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print("✅ Architecture diagrams saved as:")
    print("   - emoverse_ai_architecture.png (high-res image)")
    print("   - emoverse_ai_architecture.pdf (vector format)")
    
    return fig

if __name__ == "__main__":
    create_architecture_diagram()
    plt.show()