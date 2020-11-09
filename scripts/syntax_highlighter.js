var elements = document.getElementsByClassName('highlight'), elmnt, i;


for (elmmt = 0; elmmt < elements.length; elmmt++) {
    syntax_highlighter(elements[elmmt]);
}


function syntax_highlighter(element, _, _) {
    var lang = (element.getAttribute('data-language') || 'python').toLowerCase();
    var element_text = element.innerHTML;
    var python_colours = { text: '#d4d4d4', keyword: '#c586c0', keyword2: '#569cd6', string: '#ce9178', number: '#b5cea8', function: '#dcdcaa', class: '#4ec9b0', comment: '#6a9955' };
    if (lang == 'python') { element_text = pythonMode(element); }
    element.innerHTML = element_text;

    function pythonMode(element) {
        var rest = element.innerHTML, done = "", esc = [], i, cc, tt = "", sqstr_pos, dqstr_pos, com_pos, keyword_pos, keyword_pos2, num_pos, func_pos, class_pos, mypos, func_words, class_words;
        for (i = 0; i < rest.length; i++) {
            cc = rest.substr(i, 1);
            if (cc == "\\") {
                esc.push(rest.substr(i, 2));
                cc = "ESCAPE";
                i++;
            }
            tt += cc;
        }
        rest = tt;
        try {
            func_words = element.getAttribute('data-functions').split(',');
        } catch (error) {
            func_words = [];
        }
        try {
            class_words = element.getAttribute('data-classes').split(',');
        } catch (error) {
            class_words = [];
        }
        while (true) {
            sqstr_pos = getPos(rest, "'", "'", python_colours['string']);
            dqstr_pos = getPos(rest, '"', '"', python_colours['string']);
            com_pos = getPos(rest, '#', '\n', python_colours['comment']);
            num_pos = getNumPos(rest, python_colours['number']);
            keyword_pos = getWordPos('keyword', rest, python_colours['keyword'], []);
            keyword_pos2 = getWordPos('keyword2', rest, python_colours['keyword2'], []);
            func_pos = getWordPos('function', rest, python_colours['function'], func_words);
            class_pos = getWordPos('class', rest, python_colours['class'], class_words);
            if (Math.max(num_pos[0], sqstr_pos[0], dqstr_pos[0], com_pos[0], keyword_pos[0], keyword_pos2[0], func_pos[0], class_pos[0]) == -1) { break; }
            mypos = getMinPos(num_pos, sqstr_pos, dqstr_pos, com_pos, keyword_pos, keyword_pos2, func_pos, class_pos);
            if (mypos[0] == -1) { break; }
            if (mypos[0] > -1) {
                done += rest.substring(0, mypos[0]);
                done += colour_text(rest.substring(mypos[0], mypos[1]), mypos[2]);
                rest = rest.substr(mypos[1]);
            }
        }
        rest = done + rest;
        for (i = 0; i < esc.length; i++) {
            rest = rest.replace("ESCAPE", esc[i]);
        }
        return "<span style=color:" + python_colours['text'] + ">" + rest + "</span>";
    }
    function colour_text(text, colour) {
        return '<span style=color:' + colour + '>' + text + '</span>';
    }
    function getMinPos() {
        var i, arr = [];
        for (i = 0; i < arguments.length; i++) {
            if (arguments[i][0] > -1) {
                if (arr.length == 0 || arguments[i][0] < arr[0]) { arr = arguments[i]; }
            }
        }
        if (arr.length == 0) { arr = arguments[i]; }
        return arr;
    }
    function getWordPos(typ, text, colour, custom_words) {
        var words, i, pos, rpos = -1, rpos2 = -1, patt;
        if (lang == 'python') {
            if (typ == 'keyword') {
                words = ['as', 'assert', 'break', 'continue', 'del', 'elif', 'else', 'except', 'finally', 'for',
                    'from', 'global', 'if', 'import', 'in', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'];
            }
            else if (typ == 'keyword2') {
                words = ['and', 'class', 'def', 'False', 'is', 'lambda', 'None', 'nonlocal', 'not', 'or', 'True']
            }
            else if (typ == 'function') {
                words = ['abs', 'delattr', 'hash', 'memoryview', 'set', 'all', 'dict', 'help', 'min', 'setattr', 'any', 'dir', 'hex',
                    'next', 'slice', 'ascii', 'divmod', 'id', 'object', 'sorted', 'bin', 'enumerate', 'input', 'oct', 'staticmethod',
                    'bool', 'eval', 'int', 'open', 'str', 'breakpoint', 'exec', 'isinstance', 'ord', 'sum', 'bytearray', 'filter',
                    'issubclass', 'pow', 'super', 'bytes', 'float', 'iter', 'print', 'tuple', 'callable', 'format', 'len', 'property',
                    'type', 'chr', 'frozenset', 'list', 'range', 'vars', 'classmethod', 'getattr', 'locals', 'repr', 'zip', 'compile',
                    'globals', 'map', 'reversed', '__import__', 'complex', 'hasattr', 'max', 'round'];
            }
            else if (typ == 'class') {
                words = ['AssertionError', 'AttributeError', 'EOFError', 'FloatingPointError', 'GeneratorExit', 'ImportError',
                    'IndexError', 'KeyError', 'KeyboardInterrupt', 'MemoryError', 'NameError', 'NotImplementedError', 'OSError',
                    'OverflowError', 'ReferenceError', 'RuntimeError', 'StopIteration', 'SyntaxError', 'IndentationError',
                    'TabError', 'SystemError', 'SystemExit', 'TypeError', 'UnboundLocalError', 'UnicodeError', 'UnicodeEncodeError',
                    'UnicodeDecodeError', 'UnicodeTranslateError', 'ValueError', 'ZeroDivisionError'];
            }
        }
        words = words.concat(custom_words);
        for (i = 0; i < words.length; i++) {
            pos = text.indexOf(words[i]);
            if (pos > -1) {
                patt = /\W/g;
                if (text.substr(pos + words[i].length, 1).match(patt) && text.substr(pos - 1, 1).match(patt)) {
                    if (pos > -1 && (rpos == -1 || pos < rpos)) {
                        rpos = pos;
                        rpos2 = rpos + words[i].length;
                    }
                }
            }
        }
        return [rpos, rpos2, colour];
    }
    function getPos(text, start, end, func) {
        var s, e;
        s = text.search(start);
        e = text.indexOf(end, s + (end.length));
        if (e == -1) { e = text.length; }
        return [s, e + (end.length), func];
    }
    function getNumPos(text, func) {
        var arr = [" ", ";", "(", "+", ")", "[", "]", ",", "&", ":", "{", "}", "/", "-", "*", "|", "%", "=", "\n", "\r", "<", ">"], i, j, c, startpos = 0, endpos, word;
        for (i = 0; i < text.length; i++) {
            for (j = 0; j < arr.length; j++) {
                c = text.substr(i, arr[j].length);
                if (c == arr[j]) {
                    if (c == "-" && (text.substr(i - 1, 1) == "e" || text.substr(i - 1, 1) == "E")) {
                        continue;
                    }
                    endpos = i;
                    if (startpos < endpos) {
                        word = text.substring(startpos, endpos);
                        if (!isNaN(word)) { return [startpos, endpos, func]; }
                    }
                    i += arr[j].length;
                    startpos = i;
                    i -= 1;
                    break;
                }
            }
        }
        return [-1, -1, func];
    }
}