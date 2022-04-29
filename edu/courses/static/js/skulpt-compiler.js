const Range = ace.require("ace/range").Range;

$(document).ready(function () {
    //editor
    $(".editor").each(function (index) {
        const editor = ace.edit(this);
        editor.setTheme("ace/theme/Textmate");
        editor.session.setMode("ace/mode/python");
        editor.setFontSize("14px");
        editor.setOptions({
            enableBasicAutocompletion: true,
            enableSnippets: true,
            enableLiveAutocompletion: true,
            maxLines:15,
            minLines:6
        });
        $(this).data("aceObject", editor);
    });
    //input_area
    $(".input_data").each(function (index) {
        const input = ace.edit(this,{
            maxLines:10,
            minLines:5
        });
        input.session.setMode("ace/mode/plain_text");
        input.setFontSize("14px");
        $(this).data("aceObject", input);
    });

    //console
    $(".output").each(function (index) {
        const output = ace.edit(this,{
            maxLines:10,
            minLines:5
        });
        output.session.setMode("ace/mode/plain_text");
        output.setFontSize("14px");
        //output.renderer.setShowGutter(false);
        output.setReadOnly(true);
        $(this).data("aceObject", output);
        output.prevCursorPosition = output.getCursorPosition();

        //restrict cursor after the printed part during input
        output.selection.on("changeCursor", function () {
            const currentPosition = output.getCursorPosition();
            if (currentPosition.row < output.prevCursorPosition.row) {
                output.selection.moveCursorToPosition(output.prevCursorPosition);
            } else if (currentPosition.row == output.prevCursorPosition.row) {
                if (currentPosition.column < output.prevCursorPosition.column) {
                    output.selection.moveCursorToPosition(output.prevCursorPosition);
                }
            }
        });

        //prevent selection by double triple click during input
        output.selection.on("changeSelection", function () {
            const anchorPosition = output.selection.getSelectionAnchor();
            const leadPosition = output.selection.getSelectionLead();

            if (
                anchorPosition.row < output.prevCursorPosition.row ||
                leadPosition.row < output.prevCursorPosition.row
            ) {
                output.selection.clearSelection();
            } else if (
                anchorPosition.row == output.prevCursorPosition.row ||
                leadPosition.row == output.prevCursorPosition.row
            ) {
                if (
                    anchorPosition.column < output.prevCursorPosition.column ||
                    leadPosition.column < output.prevCursorPosition.column
                ) {
                    output.selection.clearSelection();
                }
            }
        });
    });

    //prevent selection by drag and drop during input
    $(".output").on(
        "dragstart ondrop dbclick",
        (e) => {
            e.stopImmediatePropagation();
            e.stopPropagation();
            e.preventDefault();
            return false;
        },
        false
    );
});

function builtinRead(x) {
    if (
        Sk.builtinFiles === undefined ||
        Sk.builtinFiles["files"][x] === undefined
    )
        throw "File not found: '" + x + "'";
    return Sk.builtinFiles["files"][x];
}

function* v01dInputGenerator(last) {
    var editor = ace.edit("__v01d_input_area" + last)
    const inputLines = (
        editor.session
            .getValue()
            .split("\n")
    )
    for (let line of inputLines) {
        yield line
    }
}

function runit(editorElem, outputElem) {
    $(".run-button").hide(); //hiding every runButton and turning into stop button
    $(".stop-button").show();
    const editor = $(editorElem).data("aceObject");
    const output = $(outputElem).data("aceObject");
    const prog = editor.session.getValue();
    output.session.setValue("");
    Sk.pre = "output";
    const inputLinesIter = v01dInputGenerator(editorElem.id.toString().substr(editorElem.id.toString().length - 1))

    Sk.configure({
        inputfun: () => inputLinesIter.next().value,
        output: function (text) {
            output.insert(text);
            output.prevCursorPosition = output.getCursorPosition();
            output.session.setUndoManager(new ace.UndoManager());
        },
        read: builtinRead,
        __future__: Sk.python3,
        execLimit: Number.POSITIVE_INFINITY,
    });

    $(".stop-button").on("click", function (e) {
        $(outputElem).unbind();
        output.setReadOnly(true);
        return resolve();
    });

    //(Sk.TurtleGraphics || (Sk.TurtleGraphics = {})).target = "mycanvas"; //for future pupose
    var myPromise = Sk.misceval.asyncToPromise(function () {
        return Sk.importMainWithBody("<stdin>", false, prog, true);
    });
    myPromise.then(
        function (mod) {
            console.log("success");
            $(".run-button").show();
            $(".stop-button").hide();
        },
        function (err) {
            output.insert("<" + err.toString() + ">");
            $(".run-button").show();
            $(".stop-button").hide();
        }
    );
}

function stopit() {
    Sk.execLimit = 1; //stop all previous execution

    Sk.timeoutMsg = function () {
        Sk.execLimit = Number.POSITIVE_INFINITY;
        return "Program Terminated";
    };
}