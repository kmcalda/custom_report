odoo.define("custom_report.report_view", function (require) {
  "use strict";

  console.log("Javascript module for custom_report loaded");

  var AbstractAction = require("web.AbstractAction");
  var ajax = require("web.ajax");
  var core = require("web.core");
  var QWeb = core.qweb;

  var CustomReportView = AbstractAction.extend({
    events: {
      "click .search-dist": "_onClick",
    },

    /**
     * Check tag if custom_report
     * Query all data
     * Set Variable for template use
     * Call render function
     * @param {object} parent
     * @param {object} context
     */
    init: function (parent, context) {
      this._super(parent, context);
      var self = this;
      if (context.tag == "custom_report") {
        self
          ._rpc(
            {
              model: "custom.report",
              method: "get_all",
            },
            []
          )
          .then(function (result) {
            console.log(result);
            // self.invoice_data = result;
            self.invoice_data = {};
            self.render();
            self.href = window.location.href;
          });
      }
    },

    /**
     * Load libraries
     * @returns object
     */

    willStart: function () {
      var self = this;
      return $.when(ajax.loadLibs(this), this._super());
    },

    /**
     *
     * @returns object
     */
    start: function () {
      var self = this;
      return this._super();
    },

    /**
     * Get the date value of 2 date picker
     * Query data base on the date
     * Update the table
     */
    _onClick: function () {
      var self = this;
      var date_start = $("#date-start").val();
      var date_end = $("#date-end").val();
      self
        ._rpc({
          model: "custom.report",
          method: "get_by_date",
          args: [{ date_start: date_start, date_end: date_end }],
        })
        .then(function (result) {
          var new_array = result.map(function (obj) {
            return Object.keys(obj).map(function (key) {
              return obj[key];
            });
          });
          self.tableViewReport.clear().rows.add(new_array).draw();
        });
    },

    /**
     * Call the template and append to DOM
     * Set default date to the datepicker to avoid error
     * Call previewTable function
     */
    render: function () {
      var self = this;
      var custom_report = QWeb.render("Custom_Report", {
        widget: self,
      });
      $(custom_report).prependTo(self.$el);
      var default_date = $.datepicker.formatDate("yy-mm-dd", new Date());
      $("#date-start").val(default_date);
      $("#date-end").val(default_date);
      self.previewTable();
    },

    /**
     * Instantiate the DataTables library
     *
     */
    previewTable: function () {
      var self = this;
      self.tableViewReport = $("#example").DataTable({
        dom: "Bfrtip",
        scrollX: true,
        scrollY: 650,
        buttons: [
          "copy",
          "csv",
          {
            extend: "excel",
            filename: "Odoo Report",
            title: " ",
          },
          "colvis",
        ],
        lengthMenu: [
          [10, 25, 50, -1],
          [10, 25, 50, "All"],
        ],
        pageLength: 50,
        language: {
          emptyTable: "No record found....!!!",
        },
      });
    },
  });

  /**
   * Add the custom action to the action registry
   */
  core.action_registry.add("custom_report", CustomReportView);
  return CustomReportView;
});
