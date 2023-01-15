'use strict';

const ip2bin = (ip) => ip.split(".").map(e => Number(e).toString(2).padStart(8, '0')).join('');
const ip2long = (ip) => parseInt(ip2bin(ip), 2);

const cidr2long = (cidr) => parseInt(String("").padStart(cidr, '1').padEnd(32, '0'), 2);

const getNetworkAddr = (ip, subnetmask) => (ip & subnetmask) >>> 0;
const getBroadcastAddr = (ip, subnetmask) => (ip | ~subnetmask) >>> 0;

const long2ip = (num) => {
    let bin = Number(num).toString(2).padStart(32, '0');
    return [
        bin.slice(0, 8),
        bin.slice(8, 16),
        bin.slice(16, 24),
        bin.slice(24, 32),
    ].map(e => parseInt(e, 2)).join('.');
}

const long2hostip = (num, prefix) => {
    let bin = Number(num).toString(2).padStart(32, '0');
    let list = [];
    for (let i = Math.floor(prefix/8); i < 4; i++){
        list.push(bin.slice(8*i, 8*(i+1)));
    }
    return '.'+list.map(e => parseInt(e, 2)).join('.');
}