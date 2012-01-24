import com.atlassian.jira.issue.MutableIssue
import com.atlassian.jira.component.ComponentAccessor
import com.atlassian.jira.event.type.EventDispatchOption

issue = ComponentAccessor.issueManager.getIssueObject('PHX-49') as MutableIssue
jeff = ComponentAccessor.userUtil.getUserObject('jjohnston')
sys = ComponentAccessor.userUtil.getUserObject('system')
issue.assignee = jeff
ComponentAccessor.issueManager.updateIssue(sys, issue, EventDispatchOption.ISSUE_ASSIGNED, false)