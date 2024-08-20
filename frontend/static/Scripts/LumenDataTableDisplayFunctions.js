function RenderAsDate(data) {
    if (data) { 
        const date = new Date(data);
        const formattedDate = `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}`;
        return formattedDate;
    } else { 
        return ""; 
    }
}

function RenderAsDateOnly(data) {
    if (data) { 
        const date = new Date(data);
        const formattedDate = `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
        return formattedDate;
    } else { 
        return ""; 
    }
}

function RenderValue(data) {
    if (data) { return data; } else { return ""; }
}

function RenderValueIncludingZero(data) {
    switch (data) {
        case null:
            return "";
        case 0:
            return "0";
        default:
            return data;
    }
}

function RenderNumber(data) {
    if (data != null) { return data; } else { return ""; }
}