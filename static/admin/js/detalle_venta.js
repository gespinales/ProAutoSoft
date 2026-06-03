(function () {
    'use strict';

    console.log('[DV] detalle_venta.js loaded');

    function esperarJQuery(ok) {
        if (window.django && django.jQuery) {
            ok(django.jQuery);
        } else {
            setTimeout(function () { esperarJQuery(ok); }, 50);
        }
    }

    function getJSON(url, cb) {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onload = function () { cb(JSON.parse(xhr.responseText)); };
        xhr.send();
    }

    function parseNum(str) {
        if (!str) return 0;
        str = ('' + str).trim();
        if (!str) return 0;
        var lastComma = str.lastIndexOf(',');
        var lastDot = str.lastIndexOf('.');
        if (lastComma > lastDot) {
            str = str.replace(/\./g, '').replace(',', '.');
        } else {
            str = str.replace(/,/g, '');
        }
        return parseFloat(str) || 0;
    }

    function fmtNum(n) {
        return n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    function fmtQ(n) {
        return 'Q' + fmtNum(n);
    }

    function recalcular() {
        var rows = document.querySelectorAll('#detalles-group tbody .form-row:not(.empty-form):not(.add-delete)');
        console.log('[DV] recalcular rows:', rows.length);
        var venta = 0, costo = 0;
        for (var i = 0; i < rows.length; i++) {
            var r = rows[i];
            var c = r.querySelector('[id$="-cantidad"]');
            var p = r.querySelector('[id$="-precio_unitario"]');
            var co = r.querySelector('[id$="-costo_unitario"]');
            console.log('[DV] row', i, 'cant:', c ? c.value : 'N/A', 'pu:', p ? p.value : 'N/A', 'cu:', co ? co.value : 'N/A');
            venta += parseNum(c ? c.value : '0') * parseNum(p ? p.value : '0');
            costo += parseNum(c ? c.value : '0') * parseNum(co ? co.value : '0');
        }
        var gastos = parseNum(document.getElementById('id_gastos') ? document.getElementById('id_gastos').value : '0');
        var gan = venta - costo - gastos;
        var pp = venta > 0 ? (gan / venta) * 100 : 0;
        function s(cls, v) { var e = document.querySelector('.field-' + cls + ' .readonly'); if (e) e.textContent = v; }
        s('venta_total_display', fmtQ(venta));
        s('costo_total_display', fmtQ(costo));
        s('ganancia_total_display', fmtQ(gan));
        s('ganancia_pp_display', pp.toFixed(2) + '%');
        console.log('[DV] totals: venta=' + fmtQ(venta) + ' costo=' + fmtQ(costo) + ' gan=' + fmtQ(gan) + ' pp=' + pp.toFixed(2) + '%');
    }

    function fetchPrecios(sel) {
        var id = sel.value;
        if (!id) return;
        var row = sel.closest('.form-row');
        console.log('[DV] fetchPrecios producto_id=' + id);
        getJSON('/api/productos/' + id + '/precios/', function (data) {
            console.log('[DV] API response:', JSON.stringify(data));
            var pu = row.querySelector('[id$="-precio_unitario"]');
            var cu = row.querySelector('[id$="-costo_unitario"]');
            if (pu) { pu.value = fmtNum(parseFloat(data.precio_venta)); console.log('[DV] set pu =', pu.value); }
            if (cu) { cu.value = fmtNum(parseFloat(data.costo_unitario)); console.log('[DV] set cu =', cu.value); }
            recalcular();
        });
    }

    function formatearInputs() {
        console.log('[DV] formatearInputs');
        document.querySelectorAll('#detalles-group [id$="-precio_unitario"], #detalles-group [id$="-costo_unitario"], #detalles-group [id$="-cantidad"]').forEach(function (el) {
            console.log('[DV]  input', el.id, 'original value:', '"' + el.value + '"');
            var n = parseNum(el.value);
            if (!isNaN(n) && n !== 0) {
                el.value = fmtNum(n);
                console.log('[DV]  -> formatted to', el.value);
            }
        });
    }

    function agregarBotonesEliminar() {
        document.querySelectorAll('#detalles-group tbody .has_original.form-row').forEach(function (row) {
            if (row.querySelector('.inline-deletelink')) return;
            var td = row.querySelector('td.delete');
            if (!td) return;
            var link = document.createElement('a');
            link.className = 'inline-deletelink';
            link.href = '#';
            link.title = 'Eliminar';
            link.addEventListener('click', function (e) {
                e.preventDefault();
                var cb = row.querySelector('[id$="-DELETE"]');
                if (cb) { cb.checked = true; row.classList.add('add-delete'); recalcular(); }
            });
            td.appendChild(link);
        });
    }

    esperarJQuery(function ($) {
        console.log('[DV] jQuery available, initializing...');
        var group = document.getElementById('detalles-group');
        if (!group) { console.log('[DV] ERROR: #detalles-group not found!'); return; }
        console.log('[DV] #detalles-group found');
        var $group = $(group);

        $group.on('change', 'select[id$="-producto"]', function () { console.log('[DV] producto change'); fetchPrecios(this); });
        $group.on('change input', '[id$="-cantidad"]', function () { console.log('[DV] cantidad change/input'); recalcular(); });
        $group.on('change', '[id$="-DELETE"]', function () { $(this).closest('.form-row').toggleClass('add-delete', this.checked); recalcular(); });

        group.addEventListener('formset:added', function (e) {
            if (e.detail && e.detail.formsetName === 'detalles') {
                console.log('[DV] formset:added');
                agregarBotonesEliminar(); formatearInputs(); recalcular();
            }
        });
        group.addEventListener('formset:removed', function () { console.log('[DV] formset:removed'); recalcular(); });

        var gastos = document.getElementById('id_gastos');
        if (gastos) gastos.addEventListener('input', recalcular);

        formatearInputs();
        agregarBotonesEliminar();
        recalcular();

        var form = document.getElementById('venta_form');
        if (form) {
            form.addEventListener('submit', function () {
                group.querySelectorAll('input[id$="-cantidad"], input[id$="-precio_unitario"], input[id$="-costo_unitario"]').forEach(function (el) {
                    el.value = el.value.replace(/,/g, '');
                });
                var g = document.getElementById('id_gastos');
                if (g) g.value = g.value.replace(/,/g, '');
            });
        }
    });
})();
