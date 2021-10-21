$(document).ready(function() {
    $('#table_id').DataTable({
        "order": [[ 0, "desc" ]]
    });
    $("#basic-datatable").DataTable({
        language: {
            paginate: {
                previous: "<i class='mdi mdi-chevron-left'>",
                next: "<i class='mdi mdi-chevron-right'>"
            }
        },
        drawCallback: function() {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded")
        }
    });
    var a = $("#datatable-buttons").DataTable({
        lengthChange: !1,
        buttons: ["copy", "csv", "excel", "pdf", "print"],
        // language: {
        //     paginate: {
        //         previous: "<i class='mdi mdi-chevron-left'>",
        //         next: "<i class='mdi mdi-chevron-right'>"
        //     }
        // },
        // drawCallback: function() {
        //     $(".dataTables_paginate > .pagination").addClass("pagination-rounded")
        // }
    });

    var cat = $("#datatable-buttons-cat").DataTable({
        lengthChange: !1,
        buttons: ["excel", "pdf", "print"],
        language: {
            paginate: {
                previous: "<i class='mdi mdi-chevron-left'>",
                next: "<i class='mdi mdi-chevron-right'>"
            }
        },
        drawCallback: function() {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded")
        }
    });

    var cat2 = $("#datatable-buttons-cat2").DataTable({
        lengthChange: !1,
        buttons: ["excel", "pdf", "print"],
        language: {
            paginate: {
                previous: "<i class='mdi mdi-chevron-left'>",
                next: "<i class='mdi mdi-chevron-right'>"
            }
        },
        drawCallback: function() {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded")
        }
    });

    $("#selection-datatable").DataTable({
        select: {
            style: "multi"
        },
        language: {
            paginate: {
                previous: "<i class='mdi mdi-chevron-left'>",
                next: "<i class='mdi mdi-chevron-right'>"
            }
        },
        drawCallback: function() {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded")
        }
    }),
    $("#key-datatable").DataTable({
        keys: !0,
        language: {
            paginate: {
                previous: "<i class='mdi mdi-chevron-left'>",
                next: "<i class='mdi mdi-chevron-right'>"
            }
        },
        drawCallback: function() {
            $(".dataTables_paginate > .pagination").addClass("pagination-rounded")
        }
    }),
    a.buttons().container().appendTo("#datatable-buttons_wrapper .row:eq(2)")
    cat.buttons().container().appendTo("#datatable-buttons-cat_wrapper .row:eq(2)")
    cat2.buttons().container().appendTo("#datatable-buttons-cat2_wrapper .row:eq(2)")
});
