�
    eSh  �                   �   �  G d � d�      Z y)c                   �   � e Zd Zd� Zy)�MetadataProcessorc                 �   � d}g }t        |d�      r9|j                  r-|j                  D ]  }|j                  j                  dk(  s�d}�  ||d�S )NF�entities�MessageEntityUrlT)�has_link�link_domains)�hasattrr   �	__class__�__name__)�self�messager   r   �entitys        �V/Users/kirillmozhaev/telegram-monitor/telegram_parser/processors/metadata_processor.py�processzMetadataProcessor.process   sZ   � ������7�J�'�G�,<�,<�!�*�*���#�#�,�,�0B�B�#�H� +�
 !�(�
� 	
�    N)r   �
__module__�__qualname__r   � r   r   r   r      s   � �
r   r   N)r   r   r   r   �<module>r      s   ��
� 
r   