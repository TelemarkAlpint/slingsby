(function() {

  var template = Handlebars.template, templates = Handlebars.templates = Handlebars.templates || {};

templates['articles'] = template(function (Handlebars,depth0,helpers,partials,data) {
  this.compilerInfo = [2,'>= 1.0.0-rc.3'];
helpers = helpers || Handlebars.helpers; data = data || {};
  var stack1, functionType="function", escapeExpression=this.escapeExpression, self=this;

function program1(depth0,data) {
  
  var buffer = "", stack1, stack2;
  buffer += "\r\n\r\n    <article data-datetime=\""
    + escapeExpression(((stack1 = depth0.published_date),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "\">\r\n        <h1>"
    + escapeExpression(((stack1 = depth0.title),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</h1>\r\n\r\n        ";
  stack2 = ((stack1 = depth0.content),typeof stack1 === functionType ? stack1.apply(depth0) : stack1);
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\r\n\r\n        <p>\r\n            <span class=\"byline\">Skrevet av "
    + escapeExpression(((stack1 = depth0.author),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + escapeExpression(((stack1 = depth0.published_date_as_string),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + ". </span>\r\n\r\n            ";
  stack2 = helpers['if'].call(depth0, depth0.last_edited, {hash:{},inverse:self.noop,fn:self.program(2, program2, data),data:data});
  if(stack2 || stack2 === 0) { buffer += stack2; }
  buffer += "\r\n        </p>\r\n    </article>\r\n\r\n";
  return buffer;
  }
function program2(depth0,data) {
  
  var buffer = "", stack1;
  buffer += "\r\n                <span class=\"byline\">Sist endret av "
    + escapeExpression(((stack1 = depth0.last_edited_by),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + escapeExpression(((stack1 = depth0.last_edited_datestring),typeof stack1 === functionType ? stack1.apply(depth0) : stack1))
    + "</span>\r\n            ";
  return buffer;
  }

  stack1 = helpers.each.call(depth0, depth0.articles, {hash:{},inverse:self.noop,fn:self.program(1, program1, data),data:data});
  if(stack1 || stack1 === 0) { return stack1; }
  else { return ''; }
  });
})();