from .shared_imports import *
from .plot_print_helper import plt_configure


def set_chinese_font():
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['font.serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    sns.set_style({"font.sans-serif": ['simhei', 'Arial']})

class PointClickableHTMLTooltip2(mpld3.plugins.PluginBase):
        JAVASCRIPT = """
        mpld3.register_plugin("clickablehtmltooltip", PointClickableHTMLTooltip);
        PointClickableHTMLTooltip.prototype = Object.create(mpld3.Plugin.prototype);
        PointClickableHTMLTooltip.prototype.constructor = PointClickableHTMLTooltip;
        PointClickableHTMLTooltip.prototype.requiredProps = ["id"];
        PointClickableHTMLTooltip.prototype.defaultProps = {labels:null,
                                                     targets:null,
                                                     hoffset:0,
                                                     voffset:10};
        function PointClickableHTMLTooltip(fig, props){
            mpld3.Plugin.call(this, fig, props);
        };
        PointClickableHTMLTooltip.prototype.draw = function(){
           var obj = mpld3.get_element(this.props.id);
           var labels = this.props.labels;
           var targets = this.props.targets;
           var tooltip = d3.select("body").append("div")
                        .attr("class", "mpld3-tooltip")
                        .style("position", "absolute")
                        .style("z-index", "10")
                        .style("visibility", "hidden");
           obj.elements()
               .on("mouseover", function(d, i){
                                  tooltip.html(labels[i])
                                         .style("visibility", "visible");})
                .on("mousedown", function(d, i){
                      window.open(targets[i], '_blank');
                                   })
                .on("mousemove", function(d, i){
                      tooltip
                        .style("top", d3.event.pageY + this.props.voffset + "px")
                        .style("left",d3.event.pageX + this.props.hoffset + "px");
                     }.bind(this))
                .on("mousemove", function(d, i){
                      tooltip
                        .style("top", d3.event.pageY + this.props.voffset + "px")
                        .style("left",d3.event.pageX + this.props.hoffset + "px");
                     }.bind(this))
                .on("mouseout",  function(d, i){
                               tooltip.style("visibility", "hidden");});
        };
        """

        def __init__(self, points, labels=None, targets=None,
                     hoffset=2, voffset=-6, css=None):
            self.points = points
            self.labels = labels
            self.targets = targets
            self.voffset = voffset
            self.hoffset = hoffset
            self.css_ = css or ""

            if isinstance(points, mpl.lines.Line2D):
                suffix = "pts"
            else:
                suffix = None
            self.dict_ = {"type": "clickablehtmltooltip",
                          "id": mpld3.utils.get_id(points, suffix),
                          "labels": labels,
                          "targets": targets,
                          "hoffset": hoffset,
                          "voffset": voffset}