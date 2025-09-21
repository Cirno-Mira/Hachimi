import sys
import random
import re
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QPushButton, QLabel, QMessageBox, QProgressBar,
                             QGroupBox, QGridLayout, QLineEdit, QSpinBox, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QClipboard

class HachimiVocabulary:
    """哈基米词汇库管理类"""
    def __init__(self):
        # 固定搭配
        self.phrases_df = pd.DataFrame({
            'phrase': [
                "哈基米那没路多", "阿西嘎哈呀库那路", "叮咚鸡大狗叫", "曼波马吉利",
                "哇夏马自立曼波", "哈基米打败绿豆", "吉米阿西嘎阿西", "游哒游哒曼波",
                "吉米哈压库纳鲁", "阿西噶哒布哒布", "哈基米我哪买绿豆", "阿西噶压库纳鲁",
                "哈压库阿西噶", "西哈基米米", "哟罗西库呐", "马斯塔马斯塔",
                "阿里嘎多那路", "多佐罗多佐罗", "哈耶克哈耶克", "咪西咪西"
            ],
            'length': [7, 7, 6, 5, 7, 6, 7, 6, 7, 7, 8, 7, 6, 5, 6, 6, 7, 6, 6, 5]
        })
        
        # 单词
        self.words_df = pd.DataFrame({
            'word': [
                "哈基米", "阿西嘎", "哟罗西", "哇卡鲁", "索得斯", "米娜桑", "多佐罗", "哈耶克", 
                "马斯塔", "阿里嘎", "哦莫西", "考考油", "斯国一", "乌拉拉", "咪西咪", "呀哈哟",
                "纳尼尼", "哆啦咪", "呼啦哈", "啾咪啾", "曼波", "奶龙", "叮咚", "哦曼波",
                "哈基", "阿西", "哟罗", "哇卡", "索得", "米娜", "多佐", "哈耶",
                "马斯", "阿里", "哦莫", "考考", "斯国", "乌拉", "咪西", "呀哈",
                "纳尼", "哆啦", "呼啦", "啾咪", "哈", "啊", "哟", "哇", "嗯", "咪", "西", "嘎", "鲁", "斯"
            ],
            'length': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                      2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                      2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        })
        
        # 随机性参数
        self.phrase_probability = 0.6  # 使用固定搭配的概率
        self.min_phrase_length = 4     # 使用固定搭配的最小长度
    
    def add_phrase(self, phrase, length=None):
        """添加新的固定搭配"""
        if length is None:
            length = len(phrase)
        new_row = pd.DataFrame({'phrase': [phrase], 'length': [length]})
        self.phrases_df = pd.concat([self.phrases_df, new_row], ignore_index=True)
    
    def add_word(self, word, length=None):
        """添加新的单词"""
        if length is None:
            length = len(word)
        new_row = pd.DataFrame({'word': [word], 'length': [length]})
        self.words_df = pd.concat([self.words_df, new_row], ignore_index=True)
    
    def get_phrase_by_length(self, target_length):
        """获取指定长度的固定搭配"""
        # 首先尝试找到长度完全匹配的
        exact_match = self.phrases_df[self.phrases_df['length'] == target_length]
        if not exact_match.empty:
            return random.choice(exact_match['phrase'].tolist())
        
        # 如果没有完全匹配的，找到最接近的
        self.phrases_df['diff'] = abs(self.phrases_df['length'] - target_length)
        closest = self.phrases_df.nsmallest(5, 'diff')
        return random.choice(closest['phrase'].tolist())
    
    def get_word_by_length(self, target_length):
        """获取指定长度的单词"""
        # 首先尝试找到长度完全匹配的
        exact_match = self.words_df[self.words_df['length'] == target_length]
        if not exact_match.empty:
            return random.choice(exact_match['word'].tolist())
        
        # 如果没有完全匹配的，找到最接近的
        self.words_df['diff'] = abs(self.words_df['length'] - target_length)
        closest = self.words_df.nsmallest(5, 'diff')
        return random.choice(closest['word'].tolist())
    
    def generate_hachimi_text(self, target_length):
        """生成指定长度的哈基米文本"""
        if target_length <= 0:
            return ""
        
        # 决定是否使用固定搭配
        use_phrase = (target_length >= self.min_phrase_length and 
                     random.random() < self.phrase_probability)
        
        if use_phrase:
            # 尝试使用固定搭配
            phrase = self.get_phrase_by_length(target_length)
            remaining = target_length - len(phrase)
            
            if remaining > 0:
                # 如果固定搭配不够长，添加单词
                word = self.generate_hachimi_text(remaining)
                return phrase + word
            else:
                # 如果固定搭配太长，截断
                return phrase[:target_length]
        else:
            # 使用单词组合
            if target_length <= 3:
                # 对于短文本，直接使用一个单词
                return self.get_word_by_length(target_length)
            else:
                # 对于长文本，拆分并使用多个单词
                split_point = random.randint(1, target_length-1)
                part1 = self.generate_hachimi_text(split_point)
                part2 = self.generate_hachimi_text(target_length - split_point)
                return part1 + part2


class ConversionWorker(QThread):
    """处理歌词转换的工作线程，防止界面卡顿"""
    finished = pyqtSignal(str, int, int)  # 信号：转换后的文本, 输入字符数, 输出字符数
    error = pyqtSignal(str)

    def __init__(self, input_text, vocabulary):
        super().__init__()
        self.input_text = input_text
        self.vocabulary = vocabulary

    def run(self):
        try:
            output_text, in_count, out_count = self.convert_to_hachimi(self.input_text)
            self.finished.emit(output_text, in_count, out_count)
        except Exception as e:
            self.error.emit(str(e))

    def convert_to_hachimi(self, text):
        """
        核心转换函数。
        使用哈基米词汇库生成与原始歌词相同长度的哈基米风格歌词。
        """
        # 统计输入字符数（不计空格和换行）
        input_char_count = sum(1 for char in text if char not in ' \n\r\t')
        
        # 如果是空文本，直接返回
        if not text.strip():
            return "", 0, 0
        
        lines = text.splitlines()  # 保留原换行符分割
        output_lines = []

        for line in lines:
            if not line.strip():  # 如果是空行，保留空行
                output_lines.append("")
                continue

            # 对每一行进行处理，保持原行的字符数
            line_chars = list(line)
            hachimi_chars = []
            
            # 按字符处理，但保持原标点符号
            for char in line_chars:
                if char.isspace() or not char.isalnum():
                    # 保留空格和标点符号
                    hachimi_chars.append(char)
                else:
                    # 对于非空格和非标点字符，使用哈基米字符替换
                    # 这里我们使用词汇库生成一个字符，但实际上应该根据上下文生成更长的词汇
                    # 为了简单起见，我们先生成一个字符，然后在后续步骤中调整
                    hachimi_chars.append("哈")  # 临时占位符
            
            # 将占位符替换为实际的哈基米文本
            placeholder_line = "".join(hachimi_chars)
            placeholders = re.findall(r'[^\s\W]+', placeholder_line)  # 找到所有需要替换的部分
            
            for placeholder in placeholders:
                # 为每个需要替换的部分生成哈基米文本
                hachimi_text = self.vocabulary.generate_hachimi_text(len(placeholder))
                placeholder_line = placeholder_line.replace(placeholder, hachimi_text, 1)
            
            output_lines.append(placeholder_line)

        # 用换行符连接所有行
        output_text = "\n".join(output_lines)
        # 统计输出字符数（不计空格和换行）
        output_char_count = sum(1 for char in output_text if char not in ' \n\r\t')

        return output_text, input_char_count, output_char_count


class VocabularyManager(QWidget):
    """词汇库管理界面"""
    def __init__(self, vocabulary):
        super().__init__()
        self.vocabulary = vocabulary
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('哈基米词汇库管理')
        self.setGeometry(400, 300, 600, 500)
        
        layout = QVBoxLayout()
        
        # 固定搭配管理
        phrases_group = QGroupBox("固定搭配管理")
        phrases_layout = QGridLayout()
        
        phrases_layout.addWidget(QLabel("固定搭配:"), 0, 0)
        self.phrase_input = QLineEdit()
        phrases_layout.addWidget(self.phrase_input, 0, 1)
        
        phrases_layout.addWidget(QLabel("长度:"), 1, 0)
        self.phrase_length = QSpinBox()
        self.phrase_length.setRange(1, 20)
        phrases_layout.addWidget(self.phrase_length, 1, 1)
        
        self.add_phrase_btn = QPushButton("添加固定搭配")
        self.add_phrase_btn.clicked.connect(self.add_phrase)
        phrases_layout.addWidget(self.add_phrase_btn, 2, 0, 1, 2)
        
        phrases_group.setLayout(phrases_layout)
        layout.addWidget(phrases_group)
        
        # 单词管理
        words_group = QGroupBox("单词管理")
        words_layout = QGridLayout()
        
        words_layout.addWidget(QLabel("单词:"), 0, 0)
        self.word_input = QLineEdit()
        words_layout.addWidget(self.word_input, 0, 1)
        
        words_layout.addWidget(QLabel("长度:"), 1, 0)
        self.word_length = QSpinBox()
        self.word_length.setRange(1, 10)
        words_layout.addWidget(self.word_length, 1, 1)
        
        self.add_word_btn = QPushButton("添加单词")
        self.add_word_btn.clicked.connect(self.add_word)
        words_layout.addWidget(self.add_word_btn, 2, 0, 1, 2)
        
        words_group.setLayout(words_layout)
        layout.addWidget(words_group)
        
        # 参数设置
        params_group = QGroupBox("参数设置")
        params_layout = QGridLayout()
        
        params_layout.addWidget(QLabel("使用固定搭配概率:"), 0, 0)
        self.phrase_prob = QSpinBox()
        self.phrase_prob.setRange(0, 100)
        self.phrase_prob.setValue(60)
        self.phrase_prob.setSuffix("%")
        params_layout.addWidget(self.phrase_prob, 0, 1)
        
        params_layout.addWidget(QLabel("最小固定搭配长度:"), 1, 0)
        self.min_phrase_len = QSpinBox()
        self.min_phrase_len.setRange(1, 10)
        self.min_phrase_len.setValue(4)
        params_layout.addWidget(self.min_phrase_len, 1, 1)
        
        self.save_params_btn = QPushButton("保存参数")
        self.save_params_btn.clicked.connect(self.save_params)
        params_layout.addWidget(self.save_params_btn, 2, 0, 1, 2)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # 关闭按钮
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        layout.addWidget(self.close_btn)
        
        self.setLayout(layout)
    
    def add_phrase(self):
        phrase = self.phrase_input.text().strip()
        length = self.phrase_length.value()
        
        if phrase:
            self.vocabulary.add_phrase(phrase, length)
            self.phrase_input.clear()
            QMessageBox.information(self, "成功", f"已添加固定搭配: {phrase}")
        else:
            QMessageBox.warning(self, "警告", "请输入固定搭配!")
    
    def add_word(self):
        word = self.word_input.text().strip()
        length = self.word_length.value()
        
        if word:
            self.vocabulary.add_word(word, length)
            self.word_input.clear()
            QMessageBox.information(self, "成功", f"已添加单词: {word}")
        else:
            QMessageBox.warning(self, "警告", "请输入单词!")
    
    def save_params(self):
        self.vocabulary.phrase_probability = self.phrase_prob.value() / 100.0
        self.vocabulary.min_phrase_length = self.min_phrase_len.value()
        QMessageBox.information(self, "成功", "参数已保存!")


class HachimiConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.vocabulary = HachimiVocabulary()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('哈基米歌词转换器 V1.1 Powered by Mira')
        self.setGeometry(300, 200, 1000, 700)

        # 设置全局字体和样式
        app_font = QFont("Microsoft YaHei UI" if sys.platform == "win32" else "PingFang SC", 10)
        QApplication.setFont(app_font)

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                color: #333;
            }
            QTextEdit {
                background-color: #fff;
                border: 2px solid #dce1e8;
                border-radius: 10px;
                padding: 15px;
                font-size: 13px;
                selection-background-color: #a8d1f2;
                color: #2c3e50;
            }
            QTextEdit:focus {
                border-color: #7cc2ff;
            }
            QPushButton {
                background-color: #7cc2ff;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #5aa5e0;
            }
            QPushButton:pressed {
                background-color: #3c8dbc;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #888888;
            }
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #2c3e50;
                margin: 5px;
            }
            #title {
                font-size: 26px;
                font-weight: bold;
                color: #5aa5e0;
                margin-bottom: 15px;
                padding: 10px;
                background-color: rgba(122, 194, 255, 0.1);
                border-radius: 10px;
            }
            QProgressBar {
                border: 1px solid #dce1e8;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f4f8;
                color: #2c3e50;
            }
            QProgressBar::chunk {
                background-color: #7cc2ff;
                border-radius: 5px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dce1e8;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title_label = QLabel("🐾 哈基米歌词转换器 🎵")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 输入输出区域（并排）
        io_layout = QHBoxLayout()
        io_layout.setSpacing(20)

        # 输入区域
        input_layout = QVBoxLayout()
        input_label = QLabel("📥 输入正常歌词:")
        input_layout.addWidget(input_label)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("请粘贴或输入您要转换的歌词...\n支持多行和段落。")
        input_layout.addWidget(self.input_text)
        io_layout.addLayout(input_layout)

        # 输出区域
        output_layout = QVBoxLayout()
        output_label = QLabel("📤 输出哈基米歌词:")
        output_layout.addWidget(output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("转换后的哈基米风格歌词将显示在这里...")
        output_layout.addWidget(self.output_text)
        io_layout.addLayout(output_layout)

        main_layout.addLayout(io_layout)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        self.convert_btn = QPushButton("🔄 转换")
        self.convert_btn.clicked.connect(self.start_conversion)
        self.convert_btn.setToolTip("将输入歌词转换为哈基米风格")
        button_layout.addWidget(self.convert_btn)

        self.copy_btn = QPushButton("📋 一键复制")
        self.copy_btn.clicked.connect(self.copy_output)
        self.copy_btn.setToolTip("复制输出歌词到剪贴板")
        self.copy_btn.setEnabled(False)
        button_layout.addWidget(self.copy_btn)

        self.clear_btn = QPushButton("🧹 清空")
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setToolTip("清空输入和输出区域")
        button_layout.addWidget(self.clear_btn)
        
        self.vocab_btn = QPushButton("📚 词汇库管理")
        self.vocab_btn.clicked.connect(self.open_vocabulary_manager)
        self.vocab_btn.setToolTip("管理哈基米词汇库")
        button_layout.addWidget(self.vocab_btn)

        main_layout.addLayout(button_layout)

        # 进度条（默认隐藏）
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)  # 不确定模式
        main_layout.addWidget(self.progress_bar)

        # 状态栏
        self.status_label = QLabel("🚀 就绪，请输入歌词并点击转换。")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-size: 12px; padding: 5px;")
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

        # 初始化工作线程
        self.worker = None
        self.vocab_manager = None

    def start_conversion(self):
        """开始转换歌词"""
        input_text = self.input_text.toPlainText().strip()
        if not input_text:
            QMessageBox.warning(self, "提示", "请输入要转换的歌词！")
            return

        # 禁用按钮，显示进度条
        self.set_ui_loading_state(True)
        self.status_label.setText("⏳ 正在努力转换中，请稍候...")

        # 创建并启动工作线程
        self.worker = ConversionWorker(input_text, self.vocabulary)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.error.connect(self.on_conversion_error)
        self.worker.start()

    def on_conversion_finished(self, output_text, input_count, output_count):
        """转换成功完成"""
        self.output_text.setPlainText(output_text)
        self.set_ui_loading_state(False)
        diff = abs(input_count - output_count)
        self.status_label.setText(f"✅ 转换完成！输入字符: {input_count}, 输出字符: {output_count}, 差异: {diff}")
        
        # 只有在有输出内容时才启用复制按钮
        has_output = bool(self.output_text.toPlainText().strip())
        self.copy_btn.setEnabled(has_output)

    def on_conversion_error(self, error_msg):
        """转换过程中发生错误"""
        self.set_ui_loading_state(False)
        QMessageBox.critical(self, "错误", f"转换过程中发生错误：\n{error_msg}")
        self.status_label.setText("❌ 转换出错，请重试。")

    def set_ui_loading_state(self, loading):
        """设置UI的加载状态"""
        self.convert_btn.setEnabled(not loading)
        self.clear_btn.setEnabled(not loading)
        self.vocab_btn.setEnabled(not loading)
        self.progress_bar.setVisible(loading)
        
        # 只有在非加载状态且有输出内容时才启用复制按钮
        if not loading:
            has_output = bool(self.output_text.toPlainText().strip())
            self.copy_btn.setEnabled(has_output)
        else:
            self.copy_btn.setEnabled(False)

    def copy_output(self):
        """复制输出文本到剪贴板"""
        output_text = self.output_text.toPlainText()
        if not output_text.strip():
            QMessageBox.warning(self, "提示", "没有内容可复制！")
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(output_text)
        self.status_label.setText("📋 歌词已复制到剪贴板！")

    def clear_all(self):
        """清空输入和输出"""
        self.input_text.clear()
        self.output_text.clear()
        self.copy_btn.setEnabled(False)
        self.status_label.setText("🧹 已清空，请输入新的歌词。")
    
    def open_vocabulary_manager(self):
        """打开词汇库管理界面"""
        if self.vocab_manager is None:
            self.vocab_manager = VocabularyManager(self.vocabulary)
        self.vocab_manager.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion样式使界面看起来更现代
    converter = HachimiConverter()
    converter.show()
    sys.exit(app.exec_())