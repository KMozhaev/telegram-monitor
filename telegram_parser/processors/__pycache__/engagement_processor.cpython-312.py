�
    LYh  �                   �   �  G d � d�      Z y)c                   �   � e Zd Zd� Zy)�EngagementProcessorc                 �  � t        |dd�      t        |dd�      g d�}t        |d�      r\|j                  rP|j                  j                  D ]7  }|d   j	                  |j
                  j                  |j                  d��       �9 |S )N�views�    �forwards)r   r   �	reactionsr   )�emoji�count)�getattr�hasattrr   �results�append�reaction�emoticonr
   )�self�message�
engagementr   s       �X/Users/kirillmozhaev/telegram-monitor/telegram_parser/processors/engagement_processor.py�processzEngagementProcessor.process   s�   � ��W�g�q�1����Q�7��
�
�
 �7�K�(�W�->�->�#�-�-�5�5���;�'�.�.�%�.�.�7�7�%�^�^�0� � 6�
 ��    N)�__name__�
__module__�__qualname__r   � r   r   r   r      s   � �r   r   N)r   r   r   r   �<module>r      s   ��� r   