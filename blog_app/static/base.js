
function toggle(id) {

    const blue = "#20247b";
    const orange = "#fc5356";

    if (document.getElementById(id).getAttribute("data-mark") == "true") {
        document.getElementById(id).style.background = blue;
        document.getElementById(id).setAttribute("data-mark", "false");
    } else {
        document.getElementById(id).style.background = orange;
        document.getElementById(id).setAttribute("data-mark", "true");
    }
    document.getElementById(id).style.color = "white";

}

function tag_click(id) {

    if (!window.location) {
        throw 'Unable to access window location';
    }

    toggle(id);

    search_query = window.location.search;
    const map = create_map(search_query);
    change(map, 'list_params[]', id + '', multi_values);
    change(map, 'page', '1', multi_values);
    const url = generate_url(map);
    if (url.length == 0)
        document.getElementById(id).href = '?';
    else
        document.getElementById(id).href = url;


    return false;

}

function change_page(page_no, id) {
    if (!window.location) {
        throw 'Unable to access window location';
    }
    search_query = window.location.search;
    const map = create_map(search_query);
    change(map, 'page', page_no, multi_values);
    let url = generate_url(map);
    if (url.length == 0)
        url = '?';
    console.log(url);
    document.getElementById(id).href = url;
    return false;
}

const multi_values = ['list_params[]']; //add all the multi valued query parameter here.

function create_map(url) {
    if (url.length < 2)
        return new Map();
    let index = 0;
    let prev_index = 1;
    const parts = []
    let part = 0;
    do {
        index = url.indexOf('&', index + 1);
        if (index < 0)
            part = url.slice(prev_index);
        else
            part = url.slice(prev_index, index);
        parts.push(part);
        prev_index = index + 1;
    } while (index > -1);

    const pairs = new Map();
    for (part of parts) {
        let index = part.indexOf('=');
        if (index == -1)
            throw "Invalid url (Check each key & value of query search)";
        let key = part.slice(0, index);
        let value = part.slice(index + 1);
        if (!key || !value)
            throw "Invalid url (Check each key & value of query search)";
        if (pairs.has(key)) {
            let values = pairs.get(key);
            values.add(value);
            pairs.set(key, values);
        } else {
            const set = new Set();
            set.add(value);
            pairs.set(key, set);
        }
    }

    const number_of_amp = parts.length - 1;
    index = 0;
    let number_of_equal = 0;
    do {
        index = url.indexOf('=', index + 1);
        if (index > -1)
            number_of_equal += 1;
    } while (index > -1);

    if (number_of_equal - 1 != number_of_amp)
        throw "Invalid url (Check each key & value of query search)";

    return pairs;
}

function change(pairs, key, value, multi_values) {
    if (pairs.has(key)) {
        if (isMultiValued(key)) {
            let values = pairs.get(key);
            if (values.has(value))
                values.delete(value);
            else
                values.add(value);
        } else {
            pairs.set(key, new Set([value]));
        }
    } else {
        const set = new Set();
        set.add(value);
        pairs.set(key, set);
    }


    function isMultiValued(key_item) {
        for (let value of multi_values) {
            if (value == key_item)
                return true;
        }
        return false;
    }
}

function generate_url(map) {
    let url = "?";
    map.forEach(function (values, key) {
        for (let value of values) {
            url += key + '=' + value + '&';
        }
    });
    return url.slice(0, url.length - 1);

}
