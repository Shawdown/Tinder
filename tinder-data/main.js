const bluebird = require('bluebird');
const rq = require('request');
const fs = bluebird.promisifyAll(require('fs'));
const request = bluebird.promisify(rq.defaults({ jar: true, timeout: 60000, gzip: true }));

const headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4',
    'Accept': 'application/json, text/plain, */*'
};

function checkStatus(response) {
    if (response.statusCode === 401) {
        throw new Error('401: Unathorized, insert your token in the script!');
    }
}

async function getMessages(match_id, page_token) {
    let data = [];
    let url = `https://api.gotinder.com/v2/matches/${match_id}/messages?count=100&locale=en`;
    page_token && (url += '&page_token=' + page_token);
    const response = await request({ url, headers });
    checkStatus(response);
    if (response.body) {
        let responseBody = JSON.parse(response.body);
        data = responseBody.data.messages;
        if (responseBody.data.next_page_token) {
            var others = await getMessages(match_id, responseBody.data.next_page_token);
            data = data.concat(others);
        }
    }
    return data;
}

async function getMatches(page_token) {
    let data = [];
    let url = 'https://api.gotinder.com/v2/matches?count=60&locale=en&message=1';
    page_token && (url += '&page_token=' + page_token);
    const response = await request({ url, headers });
    checkStatus(response);
    if (response.body) {
        let responseBody = JSON.parse(response.body);
        data = responseBody.data.matches;
        if (responseBody.data.next_page_token) {
            var others = await getMatches(responseBody.data.next_page_token);
            data = data.concat(others);
        }
    }
    return data;
}

async function getMatchesWithMessages() {
    const matches = await getMatches();
    return await Promise.all(matches.map(async m => {
        m.messages = await getMessages(m.id);
        m.messages = m.messages.reverse();
        return m;
    }));
}

(async () => {
    Object.assign(headers, {
        'x-auth-token': 'YOUR_TOKEN_HERE'
    });
    let data = await getMatchesWithMessages();
    data = JSON.stringify(data, null, 4);
    return await fs.writeFileAsync('./tinder.json', data, 'utf8');
})().catch(err => console.error(err));
